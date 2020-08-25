from django.db import models

# Create your models here.


class PlacePosts(models.Model):
    title = models.CharField(
        max_length=500, null=False)
    max_num = models.IntegerField(
        default=1, null=False)
    policy = models.CharField(
        max_length=500, null=False)
    introduction = models.CharField(
        max_length=500, null=False)
    is_full = models.BooleanField(
        default=False, null=False
    )
    search_code = models.CharField(max_length=2)


class RentDays(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)


class PlaceQuestions(models.Model):
    question = models.CharField(
        max_length=1000, null=False)


class PlaceReplies(models.Model):
    reply = models.CharField(
        max_length=1000, null=False)
