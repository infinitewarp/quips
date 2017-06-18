from django.conf import settings
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView

from quips.quips.models import Quip, Speaker


class QuipDetailView(DetailView):
    model = Quip

    def get_object(self, queryset=None):
        """
        Override default behavior from django.views.generic.SingleObjectMixin
        to exclusively get the Quip object by its uuid.
        """
        if queryset is None:
            queryset = self.get_queryset()

        uuid = self.kwargs.get('uuid')
        queryset = queryset.filter(uuid=uuid)

        try:
            obj = queryset.get()
        except (ValueError, queryset.model.DoesNotExist):
            # ValueError is to deal with malformed inputs that aren't valid uuids
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})

        return obj


class QuipDefaultView(QuipDetailView):
    def get_object(self, queryset=None):
        self.kwargs['uuid'] = settings.DEFAULT_QUIP_UUID
        return super(QuipDefaultView, self).get_object(queryset)


class QuipFilteredRandomView(DetailView):
    model = Quip

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = self.filter_by_speaker_id(queryset)
        return self.first_random(queryset)

    def filter_by_speaker_id(self, queryset):
        speaker_id = self.request.GET.get('speaker_id')
        if speaker_id is None:
            return queryset
        speaker = Speaker.objects.filter(id=speaker_id)
        if speaker is None:
            return queryset
        queryset = queryset.filter(quotes__speaker=speaker)
        return queryset

    def first_random(self, queryset):
        return queryset.order_by('?').first()
