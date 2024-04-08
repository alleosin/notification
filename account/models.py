from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bill = models.CharField(max_length=16)

    def __str__(self):
        return "Staronka karystalnika {}".format(self.user.username)

