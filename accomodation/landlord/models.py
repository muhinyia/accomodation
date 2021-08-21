from datetime import datetime
from django.db import models
from django.contrib.auth.models import User, Group


class Landlord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# Create your models here.
class Inquiry(models.Model):
    room = models.CharField(max_length=200)
    room_id = models.IntegerField()
    email = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user_id = models.IntegerField(blank=True)

    def __str__(self):
        return self.email
