from django.urls import path
from . import views

urlpatterns = [
    path('getAthletes/', views.getAthletes, name='getAthletes'),
    path('updateAthletes/', views.update_athlete_stats, name='updateAthletes'),
    path('', views.get_plots, name='getplots')

]