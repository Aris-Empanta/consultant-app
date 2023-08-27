from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Lawyers(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    surname = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    #instead of modifying the user model, we connnect this model to it.
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)
    specialties = models.TextField(blank=False, null=False)
    description = models.TextField()
    averageRating = models.IntegerField()
    hourlyRate = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f"Lawyer Named: {self.name}" 
    
class Clients(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    surname = models.CharField(max_length=50, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    #instead of modifying the user model, we connnect this model to it.
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)   
    
    def __str__(self):
        return f"Client Named: {self.name}" 

class Ratings(models.Model):
    client = models.OneToOneField(Clients, on_delete=models.PROTECT)
    lawyer = models.OneToOneField(Lawyers, on_delete=models.PROTECT)
    value = models.IntegerField(blank=False, null=False)