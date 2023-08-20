from django.contrib import admin

# Register your models here.
from .models import Athlete, Activity

admin.site.register(Activity)
admin.site.register(Athlete)

