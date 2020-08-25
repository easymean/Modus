from django.db import models

# Create your models here.


class ContentsPosts(models.Model):
    objects = models.Manager()
    title = models.CharField(
        max_length=500, null=False
    )
    price = models.IntegerField(
        default=0, null=False
    )
    max_num = models.IntegerField(
        default=1, null=False
    )
    introduction = models.CharField(
        max_length=2000, null=False
    )
    policy = models.CharField(
        max_length=500
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    is_end = models.BooleanField(default=False, null=False)
    is_auth = models.BooleanField(default=False, null=False)
    is_active = models.BooleanField(default=True, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)


class ContentsQuestions(models.Model):
    question = models.CharField(
        max_length=1000, null=False)


class ContentsReplies(models.Model):
    reply = models.CharField(
        max_length=1000, null=False)
