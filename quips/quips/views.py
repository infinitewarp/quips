from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.detail import DetailView

from quips.quips.models import Quip


class QuipDetailView(DetailView):
    model = Quip


class QuipRandomView(View):
    def get(self, request, *args, **kwargs):
        quip = Quip.objects.all().order_by('?').first()
        return HttpResponseRedirect(reverse("quips:detail",
                       kwargs={"pk": quip.id}))
