from django.conf import settings
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView

from quips.quips.models import Clique, Quip, Speaker


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


class QuipRandomView(DetailView):
    model = Quip

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        if queryset.count() == 0:
            raise Http404()
        return self.first_random(queryset)

    def first_random(self, queryset):
        return queryset.order_by('?').first()


class QuipRandomSpeakerView(QuipRandomView):
    def get_queryset(self):
        queryset = super(QuipRandomSpeakerView, self).get_queryset()
        queryset = self.filter_by_speaker_id(queryset)
        return queryset

    def filter_by_speaker_id(self, queryset):
        speaker_id = self.request.GET.get('speaker_id')
        if speaker_id is None:
            return queryset
        try:
            speaker = Speaker.objects.filter(pk=speaker_id).first()
            queryset = queryset.filter(quotes__speaker=speaker)
        except queryset.model.DoesNotExist:
            raise Http404()
        return queryset


class QuipRandomCliqueSpeakerView(QuipRandomView):
    template_name = 'quips/quip_detail_in_clique.html'

    def get_queryset(self):
        queryset = super(QuipRandomCliqueSpeakerView, self).get_queryset()
        queryset = self.filter_by_clique_and_speaker_id(queryset)
        return queryset

    def filter_by_clique_and_speaker_id(self, queryset):
        slug = self.kwargs.get('slug')
        speaker_id = self.request.GET.get('speaker_id')

        clique = Clique.objects.filter(slug=slug)
        speakers = Speaker.objects.filter(cliques__in=clique)
        if speaker_id is not None:
            speakers = speakers.filter(pk=speaker_id)
        queryset = queryset.filter(quotes__speaker__in=speakers)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(QuipRandomCliqueSpeakerView, self).get_context_data()
        context['slug'] = self.kwargs.get('slug')
        return context
