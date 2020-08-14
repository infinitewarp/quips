import uuid

from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from quips.quips.models import Speaker
from quips.website.templatetags.quips_extras import obfuscate_name
from quips.website.views import QuipRandomObjectBaseMixin


@method_decorator(csrf_exempt, name="dispatch")
class QuipSlackView(QuipRandomObjectBaseMixin, View):
    def get_queryset(self):
        queryset = super(QuipSlackView, self).get_queryset()
        filter_input = self.request.POST.get("text")
        if filter_input is None or len(filter_input.strip()) == 0:
            # No input? No additional filter!
            return queryset
        try:
            quip_uuid = uuid.UUID(filter_input)
            queryset = queryset.filter(uuid=quip_uuid)
            if queryset.count() == 0:
                raise QuipUuidNotFound()
        except ValueError:
            # Not a UUID? Must be a speaker name!
            queryset = self.filter_by_speaker_name(queryset, filter_input)
        return queryset

    def filter_by_speaker_name(self, queryset, speaker_name):
        try:
            speaker = Speaker.objects.filter(name__icontains=speaker_name).first()
            if speaker is None:
                raise SpeakerNameNotFound()
            queryset = queryset.filter(quotes__speaker=speaker)
        except queryset.model.DoesNotExist:
            raise SpeakerNameNotFound()
        return queryset

    @staticmethod
    def _format_quote(quote):
        if quote.speaker.should_obfuscate:
            speaker_name = obfuscate_name(str(quote.speaker))
        else:
            speaker_name = str(quote.speaker)
        if quote.is_slash_me:
            return "{} {}".format(speaker_name, quote)
        return "{}: {}".format(speaker_name, quote)

    def _build_formatted_response(self, quip, request):
        lines = [self._format_quote(quote) for quote in quip.quotes.all()]
        if quip.context:
            context = quip.context.replace("_", r"\_")
            lines.append("_{}, {}_".format(quip.date, context))
        else:
            lines.append("_{}_".format(quip.date))
        lines.append(
            request.build_absolute_uri(reverse("website:detail", args=(quip.uuid,)))
        )
        text = "\n".join(lines)
        response = {"response_type": "in_channel", "text": text}
        return response

    def post(self, request, *args, **kwargs):
        try:
            quip = self.get_object()
        except SpeakerNameNotFound:
            response = {
                "response_type": "ephemeral",
                "text": "No quips found involving speaker name like `{}`.".format(
                    request.POST.get("text")
                ),
            }
            return JsonResponse(response)
        except QuipUuidNotFound:
            response = {
                "response_type": "ephemeral",
                "text": "No quip found with UUID `{}`.".format(
                    request.POST.get("text")
                ),
            }
            return JsonResponse(response)

        response = self._build_formatted_response(quip, request)
        return JsonResponse(response)


class SpeakerNameNotFound(Exception):
    pass


class QuipUuidNotFound(Exception):
    pass
