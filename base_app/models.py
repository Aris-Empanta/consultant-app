from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    Lawyer = models.BooleanField(default=False)
    Client = models.BooleanField(default=False)

class Lawyer(models.Model):
    profile = models.OneToOneField(Profile, blank=False, on_delete=models.CASCADE, default=None)
    specialties = models.TextField(blank=False, null=False)
    description = models.TextField()
    averageRating = models.IntegerField()
    hourlyRate = models.IntegerField(blank=False, null=False)
    
class Client(models.Model):
    profile = models.OneToOneField(Profile, blank=False, on_delete=models.CASCADE, default=None)

class Rating(models.Model):
    client = models.OneToOneField(Client, on_delete=models.PROTECT)
    lawyer = models.OneToOneField(Lawyer, on_delete=models.PROTECT)
    value = models.IntegerField(blank=False, null=False)