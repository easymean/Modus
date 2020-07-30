from django.db import models
from contentsPosts.models import ContentsPosts

# Create your models here.


class Reservations(models.Model):
    PAYMENT_CHOICES = (
        ('CD', 'Card'),
        ('PH', 'Phone'),
        ('CS', 'Cash'),
    )
    user_num = models.IntegerField(
        default=1, null=False)
    is_allowed = models.BooleanField(
        default=False, null=False)
    payment_type = models.CharField(
        max_length=2, choices=PAYMENT_CHOICES)


class ContentsReviews(models.Model):
    rate = models.IntegerField(default=0, null=False)
    review = models.CharField(max_length=1000, null=False)
