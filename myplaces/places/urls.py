from django.urls import path
from . import views


app_name = "places"

urlpatterns = [
    path("", views.places_view),
    path("list/", views.ListPlacesView.as_view()),
    path("search/", views.search_places),
]


# this is for when view set is used
# from rest_framework.routers import DefaultRouter
# from . import viewsets
# router = DefaultRouter()
# router.register("", viewsets.PlaceViewset, basename="place")

# urlpatterns = router.urls
