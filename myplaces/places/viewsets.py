from rest_framework import viewsets
from .models import Place
from .serializers import DetailPlaceSerializer


class PlaceViewset(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = DetailPlaceSerializer
