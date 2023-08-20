from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Athlete
import numpy as np
import json
import requests
from utils.tokens import TOKEN
from utils.utils import fetch_activity_stats, fetch_competition_ids, update_athlete_max, update_athlete_average, average, safe_multiply

# Create your views here.



@login_required(login_url='login')
def getAthletes(request): 
    url = f"https://connect-eu.catapultsports.com/api/v6/athletes"
    headers = {"Authorization" : TOKEN}
    response = requests.get(url, headers=headers)
    
    
    try:
        athletes = response.json()

        Athlete.objects.all().delete()

        for athlete in athletes:
            athlete_inst = Athlete(
                id=athlete['id'],
                first_name=athlete['first_name'],
                last_name=athlete['last_name']
            )
            athlete_inst.save()

        messages.success(request, 'Athletes were updated')
        return render(request, 'data_checker/update_athletes.html')


    except Exception as e:
        messages.error(request, 'An error occurred during update')
        context = {'error':e}
        
        return render(request, 'data_checker/fail.html', context)

    



@login_required(login_url='login')
def update_athlete_stats(request):
    competition_ids = fetch_competition_ids()
    list_response = fetch_activity_stats(competition_ids, competition=True)

    update_athlete_max(list_response, ofparameter='total_distance', dbparameter='max_td')
    update_athlete_max(list_response, ofparameter='velocity_band1_total_distance', dbparameter='max_walking')
    update_athlete_max(list_response, ofparameter='velocity_band2_total_distance', dbparameter='max_jogging')
    update_athlete_max(list_response, ofparameter='velocity_band3_total_distance', dbparameter='max_jogging2')
    update_athlete_max(list_response, ofparameter='velocity_band4_total_distance', dbparameter='max_running')
    update_athlete_max(list_response, ofparameter='velocity_band5_total_distance', dbparameter='max_HSR')
    update_athlete_max(list_response, ofparameter='velocity_band6_total_distance', dbparameter='max_sprinting')

    update_athlete_average(list_response, ofparameter='total_distance', dbparameter='avg_td')
    update_athlete_average(list_response, ofparameter='velocity_band1_total_distance', dbparameter='avg_walking')
    update_athlete_average(list_response, ofparameter='velocity_band2_total_distance', dbparameter='avg_jogging')
    update_athlete_average(list_response, ofparameter='velocity_band3_total_distance', dbparameter='avg_jogging2')
    update_athlete_average(list_response, ofparameter='velocity_band4_total_distance', dbparameter='avg_running')
    update_athlete_average(list_response, ofparameter='velocity_band5_total_distance', dbparameter='avg_HSR')
    update_athlete_average(list_response, ofparameter='velocity_band6_total_distance', dbparameter='avg_sprinting')


    return render(request, 'data_checker/update_athletes_data.html')


@login_required(login_url='login')
def get_plots(request):
    labels = []
    data_max_td = []
    data_max_walking = []
    data_max_jogging = []
    data_max_running = []
    data_max_hsr = []
    data_max_sprinting = []

    data_temp_td = []
    data_temp_walking = []
    data_temp_jogging = []
    data_temp_running = []
    data_temp_hsr = []
    data_temp_sprinting = []


    profile = request.user.profile

    queryset  = profile.setting.athletes.all()
    
    ratio = profile.setting.get_competition_ratio_percentage

    if profile.setting.parameter == 'max':
       
        for athlete in queryset:
            labels.append(str(athlete))
            data_max_td.append(athlete.max_td)
            data_max_walking.append(athlete.max_walking)
            data_max_jogging.append(athlete.get_max_jogging)
            data_max_running.append(athlete.max_running)
            data_max_hsr.append(athlete.max_HSR)
            data_max_sprinting.append(athlete.max_sprinting)
        

    else:
        for athlete in queryset:
            labels.append(str(athlete))
            data_max_td.append(athlete.avg_td)
            data_max_walking.append(athlete.avg_walking)
            data_max_jogging.append(athlete.get_avg_jogging)
            data_max_running.append(athlete.avg_running)
            data_max_hsr.append(athlete.avg_HSR)
            data_max_sprinting.append(athlete.avg_sprinting)


    labels.append('Average')
    data_max_td.append(average(data_max_td))
    data_max_walking.append(average(data_max_walking))
    data_max_jogging.append(average(data_max_jogging))
    data_max_running.append(average(data_max_running))
    data_max_hsr.append(average(data_max_hsr))
    data_max_sprinting.append(average(data_max_sprinting))

    

    data_max_td = np.array([safe_multiply(value, ratio) for value in data_max_td])
    data_max_walking = np.array([safe_multiply(value, ratio) for value in data_max_walking])
    data_max_jogging = np.array([safe_multiply(value, ratio) for value in data_max_jogging])
    data_max_running = np.array([safe_multiply(value, ratio) for value in data_max_running])
    data_max_hsr = np.array([safe_multiply(value, ratio) for value in data_max_hsr])
    data_max_sprinting = np.array([safe_multiply(value, ratio) for value in data_max_sprinting])


    
    for athlete in queryset:
        data_temp_td.append(athlete.temp_td)
        data_temp_walking.append(athlete.temp_walking)
        data_temp_jogging.append(athlete.get_temp_jogging)
        data_temp_running.append(athlete.temp_running)
        data_temp_hsr.append(athlete.temp_HSR)
        data_temp_sprinting.append(athlete.temp_sprinting)

    data_temp_td.append(average(data_temp_td))
    data_temp_walking.append(average(data_temp_walking))
    data_temp_jogging.append(average(data_temp_jogging))
    data_temp_running.append(average(data_temp_running))
    data_temp_hsr.append(average(data_temp_hsr))
    data_temp_sprinting.append(average(data_temp_sprinting))

    

        

    context = {
        'labels':labels,
        'data_max_td':data_max_td.tolist(),
        'data_max_walking':data_max_walking.tolist(),
        'data_max_jogging':data_max_jogging.tolist(),
        'data_max_running':data_max_running.tolist(),
        'data_max_hsr':data_max_hsr.tolist(),
        'data_max_sprinting':data_max_sprinting.tolist(),

        'data_temp_td':data_temp_td,
        'data_temp_walking':data_temp_walking,
        'data_temp_jogging':data_temp_jogging,
        'data_temp_running':data_temp_running,
        'data_temp_hsr':data_temp_hsr,
        'data_temp_sprinting':data_temp_sprinting,


    }

    return render(request, 'data_checker/plots.html', context)

