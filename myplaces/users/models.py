from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars", blank=True)
    superhost = models.BooleanField(default=False)
    favs = models.ManyToManyField("places.Place", related_name="favs")

    def places_count(self):
        return self.places.count()

    places_count.short_description = "Place Count"
