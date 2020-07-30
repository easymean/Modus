from django.db import models
# Create your models here.


class Places(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
    )
    location = models.CharField(
        max_length=250,
        null=False,
    )
    image = models.CharField(
        max_length=500,
        null=True,
    )
    create_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
