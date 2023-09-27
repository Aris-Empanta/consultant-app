from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Profile(models.Model):
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, default="avatar.svg")
    Lawyer = models.BooleanField(default=False)
    Client = models.BooleanField(default=False)

class Lawyer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, default=None)
    areasOfExpertise = models.TextField()
    city = models.TextField()
    yearsOfExperience = models.IntegerField(default=0)
    description = models.TextField()
    averageRating = models.IntegerField(default=0)
    hourlyRate = models.IntegerField(default=0)
    
class Client(models.Model):
    profile = models.OneToOneField(Profile, blank=False, on_delete=models.CASCADE, default=None)

class Rating(models.Model):
    client = models.OneToOneField(Client, on_delete=models.PROTECT)
    lawyer = models.OneToOneField(Lawyer, on_delete=models.PROTECT)
    value = models.IntegerField(blank=False, default=0)