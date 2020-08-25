from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    user = RelatedUserSerializer(read_only=True)
    is_fav = serializers.SerializerMethodField(
        method_name="is_fav"
    )  # append "get_" and make def

    class Meta:
        model = Place
        exclude = "modified"
        read_only_fields = "user"

    def validate(self, data):
        if self.instance:  # when update data
            check_in = data.get("check_in", self.instance.check_in)  # la is default
            check_out = data.get("check_out", self.instance.check_out)  # la is default
        else:  # when create data
            check_in = data.get("check_in")
            check_out = data.get("check_out")

        if check_out >= check_in:
            raise serializers.ValidationError("not enough time")

        return data  # must always return data

    def is_fav(self, obj):  # obj is current place
        request = self.context.get("request")

        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False

    def create(self, validated_data):
        request = self.context.get("request")
        place = Place.objects.create(**validated_data, user=request.user)
        return place


class DetailPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        exclude = "modified"


class CreatePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        exclude = ("user", "modified", "created")

    def validate(self, data):
        if self.instance:  # when update data
            check_in = data.get("check_in", self.instance.check_in)  # la is default
            check_out = data.get("check_out", self.instance.check_out)  # la is default
        else:  # when create data
            check_in = data.get("check_in")
            check_out = data.get("check_out")

        if check_out >= check_in:
            raise serializers.ValidationError("not enough time")

        return data  # must always return data

    # save()를 통해 상황에 따라 create / update가 실행됩니다.
    # def create(self, validated_data):
    #     return Place.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.address = validated_data.get("address", instance.address)
    #     instance.price = validated_data.get("price", instance.price)
    #     instance.lat = validated_data.get("lat", instance.lat)
    #     instance.lng = validated_data.get("lng", instance.lng)
    #     instance.check_in = validated_data.get("check_in", instance.check_in)
    #     instance.check_out = validated_data.get("check_out", instance.check_out)
    #     instance.instant_book = validated_data.get(
    #         "instant_book", instance.instant_book
    #     )
    #     instance.save()
    #     return instance
