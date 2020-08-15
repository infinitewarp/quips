"""View functionality to handle Slack's slash-command requests."""

from django.http import Http404, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from quips.quips.anonymize import obfuscate_name
from quips.quips.filters import (
    InputNotValidUUID,
    filter_by_speaker_name,
    filter_by_uuid,
)
from quips.website.views import QuipRandomObjectBaseMixin


def stringify_quote(quote):
    """Format a Quip's Quote into a single line string."""
    if quote.speaker.should_obfuscate:
        speaker_name = obfuscate_name(str(quote.speaker))
    else:
        speaker_name = str(quote.speaker)
    if quote.is_slash_me:
        return f"{speaker_name} {quote}"
    return f"{speaker_name}: {quote}"


def format_response_quip(quip, quip_absolute_uri):
    """Format a typical in-channel response containing a whole Quip."""
    lines = [stringify_quote(quote) for quote in quip.quotes.all()]
    if quip.context:
        context = quip.context.replace("_", r"\_")
        lines.append(f"_{quip.date}, {context}_")
    else:
        lines.append(f"_{quip.date}_")
    lines.append(quip_absolute_uri)
    text = "\n".join(lines)
    response = {"response_type": "in_channel", "text": text}
    return response


def format_response_not_found_error(command_text):
    """Format an ephemeral error when no Quip is found."""
    response = {
        "response_type": "ephemeral",
        "text": f"No quip found for `{command_text}`.",
    }
    return response


@method_decorator(csrf_exempt, name="dispatch")
class QuipSlackView(QuipRandomObjectBaseMixin, View):
    """View to handle a Slack app's slash-command integration."""

    def get_command_text(self):
        """Get the slash-command payload's main text component."""
        return self.request.POST.get("text", "").strip()

    def get_queryset(self):
        """
        Get the Quip queryset with additional filters applied.

        If no input is given, use the default queryset for any Quip.
        If the input appears to be a UUID, filter on Quip's UUID.
        Else, filter assuming the input is a Speaker's name (or part of one).
        """
        queryset = super(QuipSlackView, self).get_queryset()
        filter_input = self.get_command_text()
        if not filter_input:
            # No input? Just return any quip without filtering.
            return queryset
        try:
            queryset = filter_by_uuid(queryset, filter_input)
        except InputNotValidUUID:
            queryset = filter_by_speaker_name(queryset, filter_input)
        return queryset

    def post(self, request, *args, **kwargs):
        """Handle Slack's typical POST request."""
        try:
            quip = self.get_object()
        except Http404:
            quip = None
        if quip:
            quip_absolute_uri = request.build_absolute_uri(
                reverse("website:detail", args=(quip.uuid,))
            )
            response = format_response_quip(quip, quip_absolute_uri)
        else:
            command_text = self.get_command_text()
            response = format_response_not_found_error(command_text)
        return JsonResponse(response)
