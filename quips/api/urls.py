from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"speaker", views.SpeakerViewSet)
router.register(r"clique", views.CliqueViewSet)
router.register(r"stats", views.StatsViewSet, basename="stats")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
