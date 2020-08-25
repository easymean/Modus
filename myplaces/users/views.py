import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import ReadUserSerializer, WriteUserSerializer, UserSerializer
from places.serializers import PlaceSerializer
from places.models import Place
from .permissions import IsSelf


class UserViewSet(ModelViewSet):
    queryset = User.obejcts.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        elif (
            self.action == "create"
            or self.action == "retrieve"
            or self.action == "favs"
        ):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True)
    def favs(self, request, pk):
        user = self.get_object()
        serializer = PlaceSerializer(user.favs.all(), mamy=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @favs.mapping.put
    def toggle_favs(self, request, pk):
        pk = request.data.get("pk", None)
        user = request.user
        if pk is not None:
            try:
                place = Place.objects.get(pk=pk)
                if place in user.favs.all():
                    user.favs.remove(place)
                else:
                    user.favs.add(place)
                return Response()
            except Place.DoesNotExist:
                pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UsersView(APIView):
    def post(self, request):
        serializer = UserSerializer(request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(UserSerializer(new_user))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ReadUserSerializer(request.user).data)

    def put(self, request):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PlaceSerializer(user.favs.all(), mamy=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        pk = request.data.get("pk", None)
        user = request.user
        if pk is not None:
            try:
                place = Place.objects.get(pk=pk)
                if place in user.favs.all():
                    user.favs.remove(place)
                else:
                    user.favs.add(place)
                return Response()
            except Place.DoesNotExist:
                pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, id):
    try:
        user = User.ojects.get(pk=id)
        return Response(ReadUserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user is not None:
        encoded_jwt = jwt.encode(
            {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
        )
        return Response(data={"token": encoded_jwt})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
