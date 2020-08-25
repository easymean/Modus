from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Place
from .serializers import PlaceSerializer, DetailPlaceSerializer, CreatePlaceSerializer
from .permissions import IsOwner


class OwnPagination(PageNumberPagination):
    page_size = 20


class ListPlacesView(APIView):
    def get(self, request):
        paginator = OwnPagination()
        places = Place.objects.all()
        results = paginator.paginate_queryset(places, request)
        serializer = PlaceSerializer(
            results, many=True, context={"request": request}
        ).data
        return paginator.get_paginated_response(serializer)


class PlaceView(APIView):
    def get_place(self, id):
        try:
            place = Place.objects.get(pk=id)
            return place
        except Place.DoesNotExist:
            return None

    def get(self, request, id):
        place = self.get_place(id)
        if place is not None:
            serializer = DetailPlaceSerializer(place).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = CreatePlaceSerializer(data=request.data)

        if serializer.is_valid():
            place = serializer.save(user=request.user)
            place_serializer = DetailPlaceSerializer(place).data
            return Response(data=place_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        place = self.get_place(id)

        if place is not None:
            if place.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = CreatePlaceSerializer(
                place, data=request.data, partial=True
            ).data
            if serializer.is_valid():
                place = serializer.save()
                place_serializer = DetailPlaceSerializer(place).data
                return Response(place_serializer, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        place = self.get_place(id)

        if place is not None:
            if place.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            place.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def search_places(request):
    max_price = request.GET.get("max_price", None)  # get params
    min_price = request.GET.get("min_price", None)
    lat = request.GET.get("lat", None)
    lng = request.GET.get("lng", None)

    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs["price__lte"] = max_price

    if min_price is not None:
        filter_kwargs["price__gte"] = min_price

    if lat is not None and lng is not None:
        filter_kwargs["lat__gte"] = lat - 0.005
        filter_kwargs["lat__lte"] = lat + 0.005
        filter_kwargs["lng__gte"] = lng - 0.005
        filter_kwargs["lng__lte"] = lng + 0.005

    paginator = PageNumberPagination()
    paginator.page_size = 20

    try:
        places = Place.objects.filter(**filter_kwargs)  # unpacking
    except ValueError:
        places = Place.objects.all()

    results = paginator.paginate_queryset(places, request)
    serializer = PlaceSerializer(results, many=True).data
    return paginator.get_paginated_response(serializer)


# viewset
class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    pagination_class = OwnPagination()

    def get_permissions(self):

        if self.action == "list" or self.action == "retrieve":
            # get a room or rooms
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def search(self, request):
        max_price = request.GET.get("max_price", None)  # get params
        min_price = request.GET.get("min_price", None)
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)

        filter_kwargs = {}
        if max_price is not None:
            filter_kwargs["price__lte"] = max_price

        if min_price is not None:
            filter_kwargs["price__gte"] = min_price

        if lat is not None and lng is not None:
            filter_kwargs["lat__gte"] = lat - 0.005
            filter_kwargs["lat__lte"] = lat + 0.005
            filter_kwargs["lng__gte"] = lng - 0.005
            filter_kwargs["lng__lte"] = lng + 0.005

        try:
            places = Place.objects.filter(**filter_kwargs)  # unpacking
        except ValueError:
            places = Place.objects.all()
        paginator = self.pagination_class
        results = paginator.paginate_queryset(places, request)
        serializer = PlaceSerializer(results, many=True).data
        return paginator.get_paginated_response(serializer)


# generic view
class ListPlacesView2(ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class DetailPlaceView2(RetrieveAPIView):
    queryset = Place.objects.all()
    serializer_class = DetailPlaceSerializer
    lookup_url_kwarg = "id"  # url에 pk면 필요없음


# def
@api_view(["GET", "POST"])
def list_places(request):
    places = Place.objects.all()
    serialized_places = PlaceSerializer(places, many=True)
    return Response(data=serialized_places.data)


@api_view(["GET", "POST"])
def places_view(request):
    if request.method == "GET":
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True).data
        return Response(serializer)
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = CreatePlaceSerializer(data=request.data)

        if serializer.is_valid():
            place = serializer.save(user=request.user)
            place_serializer = DetailPlaceSerializer(place).data
            return Response(data=place_serializer, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.error, status=status.HTTP_400_BAD_REQUEST)

