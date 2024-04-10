# Create your models here.
from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bill = models.CharField(max_length=16)

    def __str__(self):
        return "Staronka karystalnika {}".format(self.user.username)


class Notification(models.Model):
    sender = models.CharField(max_length=20, blank=True)
    addressee = models.ForeignKey(Profile, related_name="notifications", on_delete=models.CASCADE)
    endowment = models.DecimalField(max_digits=10, decimal_places=2)
    text = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
