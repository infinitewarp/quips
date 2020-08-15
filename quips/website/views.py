import random

from django.conf import settings
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView, SingleObjectMixin

from quips.quips.filters import (
    InputNotValidUUID,
    filter_by_clique,
    filter_by_speaker_id,
    filter_by_uuid,
)
from quips.quips.models import Quip


class QuipDetailView(DetailView):
    model = Quip

    def get_object(self, queryset=None):
        """
        Return the Quip object the view is displaying.

        Override default behavior from django.views.generic.SingleObjectMixin
        to exclusively get the Quip object by its uuid.
        """
        if queryset is None:
            queryset = self.get_queryset()

        uuid_string = self.kwargs.get("uuid")
        try:
            quip = filter_by_uuid(queryset, uuid_string).get()
        except InputNotValidUUID:
            raise Http404(
                _("No %(verbose_name)s found matching the query")
                % {"verbose_name": self.model._meta.verbose_name}
            )
        return quip


class QuipDefaultView(QuipDetailView):
    def get_object(self, queryset=None):
        self.kwargs["uuid"] = settings.DEFAULT_QUIP_UUID
        return super(QuipDefaultView, self).get_object(queryset)


class QuipRandomObjectBaseMixin(SingleObjectMixin):
    model = Quip

    def get_object(self, queryset=None):
        """
        Get the random Quip object.

        Note for historic context: This function used to add calls to
        the base queryset `.order_by("?").first()` to get one shuffled
        item from the database. Unfortunately, some of our queries have
        grown so complex (see: `filter_by_clique`) that the Django query
        builder breaks and cannot use that style of random ordering. So,
        we have to find a random offset ourselves. This potentially comes
        with some cost of executing arguably unnecessary additional DB
        queries, but at least it works.
        """
        if queryset is None:
            queryset = self.get_queryset()
        result_count = queryset.count()
        if result_count == 0:
            raise Http404()
        random_offset = random.randrange(0, result_count)
        return queryset.order_by("id")[random_offset]


class QuipRandomView(QuipRandomObjectBaseMixin, DetailView):
    pass


class QuipRandomSpeakerView(QuipRandomView):
    def get_queryset(self):
        queryset = super(QuipRandomSpeakerView, self).get_queryset()
        speaker_id = self.request.GET.get("speaker_id")
        if speaker_id:
            queryset = filter_by_speaker_id(queryset, speaker_id)
        return queryset


class QuipRandomCliqueSpeakerView(QuipRandomView):
    template_name = "quips/quip_detail_in_clique.html"

    def get_queryset(self):
        queryset = super(QuipRandomCliqueSpeakerView, self).get_queryset()
        clique_slug = self.kwargs.get("slug")
        if not clique_slug:
            raise Http404()
        speaker_id = self.request.GET.get("speaker_id")
        if speaker_id:
            queryset = filter_by_speaker_id(queryset, speaker_id)
        queryset = filter_by_clique(queryset, clique_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuipRandomCliqueSpeakerView, self).get_context_data()
        context["slug"] = self.kwargs.get("slug")
        return context
