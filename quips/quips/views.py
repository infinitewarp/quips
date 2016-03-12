from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.detail import DetailView

from quips.quips.models import Quip


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


class QuipRandomView(View):
    def get(self, request, *args, **kwargs):
        quip = Quip.objects.all().order_by('?').first()
        if not quip:
            raise Http404()
        return HttpResponseRedirect(reverse("quips:detail",
                       kwargs={"uuid": quip.uuid}))
