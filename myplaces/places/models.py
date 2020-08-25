from django.db import models
from common.models import Common


class Place(Common):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    price = models.IntegerField(help_text="won per night")
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lng = models.DecimalField(max_digits=10, decimal_places=6)
    check_in = models.TimeField(default="00:00:00")
    check_out = models.TimeField(default="00:00:00")
    instant_book = models.BooleanField(default=False)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="places"
    )

    def __str__(self):
        return self.name

    def photo_number(self):
        return self.photos.count()

    photo_number.short_description = "Photo Count"

    class Meta:
        ordering = ["-pk"]


class Photo(Common):

    file = models.ImageField()
    place = models.ForeignKey(
        "places.Place", related_name="photos", on_delete=models.CASCADE
    )
    caption = models.CharField(max_length=140)

    def __str__(self):
        return self.place.name
