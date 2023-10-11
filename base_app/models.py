from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator 

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
    city = models.CharField(max_length=50, null=True)
    yearsOfExperience = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(80)])
    description = models.TextField(null=True)
    averageRating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    hourlyRate = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    address = models.CharField(max_length=50, null=True)
    lisenceStatus = models.CharField(max_length=20,null=True, choices=(
                                                                ("active", "active"),
                                                                ("suspended", "suspended"),
                                                                ("revoked", "revoked")
                                                            ), default=("active", "active"))
    phone = models.CharField(max_length=20, null=True)

class AvailableHours(models.Model):
    lawyer = models.OneToOneField(Lawyer, on_delete=models.PROTECT)
    startingTime = models.DateTimeField(null=True)
    endingTime = models.DateField(null=True)

class Appointments(models.Model):
    interval = models.ForeignKey(AvailableHours, on_delete=models.CASCADE)
    booked = models.BooleanField(default=False)
    startingTime = models.DateTimeField(null=True)
    endingTime = models.DateField(null=True)

class Client(models.Model):
    profile = models.OneToOneField(Profile, blank=False, on_delete=models.CASCADE, default=None)

class Rating(models.Model):
    client = models.OneToOneField(Client, on_delete=models.PROTECT)
    lawyer = models.OneToOneField(Lawyer, on_delete=models.PROTECT)
    value = models.IntegerField(blank=False, default=0)