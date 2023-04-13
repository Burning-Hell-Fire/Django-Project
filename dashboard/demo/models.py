# In models.py

from django.db import models
from django.contrib.auth.models import User
from dashboard import settings

class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, default=0)
    dob = models.DateField()
    city = models.CharField(max_length=255, blank=True, default='')
    country = models.CharField(max_length=255, blank=True, default='')
    state = models.CharField(max_length=255,blank=True, default='')
    phone_number = models.IntegerField(null=True, default=0)
    class Meta:
        unique_together = (("user", "name"),)
    def __str__(self):
        return self.user.username
class Image(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image/',null=True, default='default_image.png')
    def __str__(self):
        return self.user.username