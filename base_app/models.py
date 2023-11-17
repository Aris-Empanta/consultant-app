from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator 

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Profile(models.Model):
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, default="avatar.png", upload_to='images/profile-pics/')
    Lawyer = models.BooleanField(default=False)
    Client = models.BooleanField(default=False)

    def __str__(self):
        return f'This is the Profile object of {self.user.first_name} {self.user.last_name}'

class Lawyer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
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

    def __str__(self):
        return f'This is the Lawyer object of {self.profile.user.first_name} {self.profile.user.last_name}'

class Client(models.Model):
    profile = models.OneToOneField(Profile, blank=False, on_delete=models.CASCADE, default=None)

class AvailableHours(models.Model):
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE)
    starting_time = models.DateTimeField(null=True)
    ending_time = models.DateTimeField(null=True)

class Appointments(models.Model):
    interval = models.ForeignKey(AvailableHours, on_delete=models.CASCADE)
    lawyer = models.ForeignKey(Lawyer, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    booked = models.BooleanField(default=False)
    starting_time = models.DateTimeField(null=True)
    ending_time = models.DateTimeField(null=True)
    checked = models.BooleanField(default=False)
    time_booked = models.DateTimeField(null=True)
    informed_client = models.BooleanField(default=False)

class Rating(models.Model):
    client = models.OneToOneField(Client, on_delete=models.PROTECT)
    lawyer = models.OneToOneField(Lawyer, on_delete=models.PROTECT)
    value = models.IntegerField(blank=False, default=0)
    comments = models.TextField(null=True)

class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=150, null=True)    
    time_sent = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=False)
    read = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)