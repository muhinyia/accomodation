from django.db import models
from datetime import datetime
from landlord.models import Landlord


class Room(models.Model):
    statuses = (('under review', 'under review'),
                ('approved', 'approved'),
                ('submitted', 'submitted'),
                ('rejected', 'rejected'),)
    landlord = models.ForeignKey(Landlord, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    description = models.TextField()
    rent = models.IntegerField()
    bond_amount = models.IntegerField()
    size = models.IntegerField()
    photo_main = models.ImageField(upload_to='rooms/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='rooms/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='rooms/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='rooms/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='rooms/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='rooms/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='rooms/%Y/%m/%d/', blank=True)
    photo_7 = models.ImageField(upload_to='rooms/%Y/%m/%d/', blank=True)
    photo_8 = models.ImageField(upload_to='rooms/%Y/%m/%d/', blank=True)
    photo_9 = models.ImageField(upload_to='rooms/%Y/%m/%d/', blank=True)
    is_available = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=statuses)
    list_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.title
