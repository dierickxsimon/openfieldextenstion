from django.db import models
from django.contrib.auth.models import User
from data_checker.models import Athlete
import uuid

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    setting = models.OneToOneField('Setting', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                           primary_key=True, editable=False)
    
    def __str__(self):
        return str(self.user.username)
    
  
    

class Setting(models.Model):
    CHOICES = [
        ('max', 'Maximal Distance'),
        ('avg', 'Average Distance')
    ]


    athletes = models.ManyToManyField(Athlete, blank=True)
    start_date = models.DateField(default='1990-01-01') 
    end_date = models.DateField(default = '1990-02-01')
    parameter = models.CharField(max_length=50, choices=CHOICES)
    competition_ratio = models.IntegerField(default=100)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                           primary_key=True, editable=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_competition_ratio_percentage(self):
        percentage = self.competition_ratio/100
        return percentage



