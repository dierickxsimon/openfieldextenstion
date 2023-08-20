from django.db import models
import uuid

# Create your models here.
class Activity(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True)
    competition = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                           primary_key=True, editable=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date']
    

class Athlete(models.Model):
    first_name = models.CharField(max_length=300, null=True, blank=True)
    last_name = models.CharField(max_length=300, null=True, blank=True)
    max_td = models.IntegerField(default=0, null=True, blank=True)
    max_sprinting = models.IntegerField(default=0, null=True, blank=True)
    max_HSR = models.IntegerField(default=0, null=True, blank=True)
    max_running = models.IntegerField(default=0, null=True, blank=True)
    max_jogging = models.IntegerField( default=0, null=True, blank=True)
    max_jogging2 = models.IntegerField( default=0, null=True, blank=True)
    max_walking = models.IntegerField(default=0, null=True, blank=True)
    avg_td = models.IntegerField(default=0, null=True, blank=True)
    avg_sprinting = models.IntegerField(default=0, null=True, blank=True)
    avg_HSR = models.IntegerField(default=0, null=True, blank=True)
    avg_running = models.IntegerField(default=0, null=True, blank=True)
    avg_jogging = models.IntegerField(default=0, null=True, blank=True)
    avg_jogging2 = models.IntegerField(default=0, null=True, blank=True)
    avg_walking = models.IntegerField(default=0, null=True, blank=True)
    temp_td = models.IntegerField(default=0, null=True, blank=True)
    temp_sprinting = models.IntegerField(default=0, null=True, blank=True)
    temp_HSR = models.IntegerField(default=0, null=True, blank=True)
    temp_running = models.IntegerField(default=0, null=True, blank=True)
    temp_jogging = models.IntegerField( default=0, null=True, blank=True)
    temp_jogging2 = models.IntegerField( default=0, null=True, blank=True)
    temp_walking = models.IntegerField(default=0, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                           primary_key=True, editable=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-max_td']
    
    @property
    def get_max_jogging(self):
        jogging = self.max_jogging + self.max_jogging2
        return jogging
    
    @property
    def get_avg_jogging(self):
        jogging = self.avg_jogging + self.avg_jogging2
        return jogging
    
    @property
    def get_temp_jogging(self):
        jogging = self.temp_jogging + self.temp_jogging2
        return jogging


    



    
   