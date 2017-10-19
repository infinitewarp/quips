from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView, SingleObjectMixin

from quips.quips.models import Clique, Quip, Speaker
from quips.quips.templatetags.quips_extras import obfuscate_name


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
        try:
            queryset = queryset.filter(uuid=uuid)
            obj = queryset.get()
        except (ValidationError, ValueError, queryset.model.DoesNotExist):
            # ValidationError and ValueError are to deal with malformed inputs
            # that aren't valid uuids.
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})

        return obj


class QuipDefaultView(QuipDetailView):
    def get_object(self, queryset=None):
        self.kwargs['uuid'] = settings.DEFAULT_QUIP_UUID
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
        return queryset.order_by('?').first()


class QuipRandomView(QuipRandomObjectBaseMixin, DetailView):
    pass


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


@method_decorator(csrf_exempt, name='dispatch')
class QuipSlackView(QuipRandomObjectBaseMixin, View):
    @staticmethod
    def _format_quote(quote):
        if quote.is_slash_me:
            return '{} {}'.format(obfuscate_name(str(quote.speaker)), quote)
        return '{}: {}'.format(obfuscate_name(str(quote.speaker)), quote)

    def post(self, request, *args, **kwargs):
        quip = self.get_object()
        lines = [self._format_quote(quote) for quote in quip.quotes.all()]
        if quip.context:
            context = quip.context.replace('_', r'\_')
            lines.append('_{}, {}_'.format(quip.date, context))
        else:
            lines.append('_{}_'.format(quip.date))
        lines.append(request.build_absolute_uri(reverse('quips:detail', args=(quip.uuid,))))
        text = '\n'.join(lines)
        response = {
            "response_type": "in_channel",
            "text": text,
        }
        return JsonResponse(response)
