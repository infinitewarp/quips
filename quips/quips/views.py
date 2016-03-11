from django.views.generic.detail import DetailView

from quips.quips.models import Quip


class QuipDetailView(DetailView):
    model = Quip
