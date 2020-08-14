from django.conf import settings
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView, SingleObjectMixin

from quips.quips.filters import (
    InputNotValidUUID,
    QuipUuidNotFound,
    filter_by_clique_and_speaker_id,
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
        except (InputNotValidUUID, QuipUuidNotFound, queryset.model.DoesNotExist):
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
        if queryset is None:
            queryset = self.get_queryset()
        if queryset.count() == 0:
            raise Http404()
        return self.first_random(queryset)

    def first_random(self, queryset):
        return queryset.order_by("?").first()


class QuipRandomView(QuipRandomObjectBaseMixin, DetailView):
    pass


class QuipRandomSpeakerView(QuipRandomView):
    def get_queryset(self):
        queryset = super(QuipRandomSpeakerView, self).get_queryset()
        speaker_id = self.request.GET.get("speaker_id")
        try:
            queryset = filter_by_speaker_id(queryset, speaker_id)
        except queryset.model.DoesNotExist:
            raise Http404()
        return queryset


class QuipRandomCliqueSpeakerView(QuipRandomView):
    template_name = "quips/quip_detail_in_clique.html"

    def get_queryset(self):
        queryset = super(QuipRandomCliqueSpeakerView, self).get_queryset()
        clique_slug = self.kwargs.get("slug")
        speaker_id = self.request.GET.get("speaker_id")
        queryset = filter_by_clique_and_speaker_id(queryset, clique_slug, speaker_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuipRandomCliqueSpeakerView, self).get_context_data()
        context["slug"] = self.kwargs.get("slug")
        return context
