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

LISENCE_STATUSES = (
    ("active", "active"),
    ("suspended", "suspended"),
    ("revoked", "revoked")
)

class Lawyer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, default=None)
    areasOfExpertise = models.TextField(null=True)
    city = models.TextField(null=True)
    yearsOfExperience = models.IntegerField(default=0)
    description = models.TextField(null=True)
    averageRating = models.IntegerField(default=0)
    hourlyRate = models.IntegerField(default=0)
    address = models.TextField(null=True)
    lisenceStatus = models.CharField(max_length=20,null=True, choices=(
                                                                ("active", "active"),
                                                                ("suspended", "suspended"),
                                                                ("revoked", "revoked")
                                                            ))
    phone = models.CharField(max_length=20, null=True)
    
    
class Client(models.Model):
    profile = models.OneToOneField(Profile, blank=False, on_delete=models.CASCADE, default=None)

class Rating(models.Model):
    client = models.OneToOneField(Client, on_delete=models.PROTECT)
    lawyer = models.OneToOneField(Lawyer, on_delete=models.PROTECT)
    value = models.IntegerField(blank=False, default=0)