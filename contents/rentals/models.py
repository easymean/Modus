from django.db import models

# Create your models here.


class Rentals(models.Model):
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(auto_now_add=True)
    user_num = models.IntegerField(default=1, null=False)
    is_allowed = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)


class PlaceReviews(models.Model):
    rate = models.IntegerField(default=0, null=False)
    review = models.CharField(max_length=1000, null=False)
