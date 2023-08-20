# utils.py
import requests
from profiles.models import Athlete
from .tokens import TOKEN

def fetch_competition_ids():
    url = "https://connect-eu.catapultsports.com/api/v6/activities?sort=-start_time"
    headers = {
        "accept": "application/json",
        "authorization": TOKEN
    }

    response = requests.get(url, headers=headers)
    activities = response.json()
    competitions = [activity for activity in activities if "wedstrijd" in activity["tags"]]
    first_10_competition_ids = [competition["id"] for competition in competitions[:10]]
    return first_10_competition_ids


from datetime import datetime

def convert_to_posix(date_str):
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        posix_timestamp = int(dt.timestamp())
        return posix_timestamp
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."


def fetch_non_competition_activity_ids(start_date, end_date):
    psoix_start_date = convert_to_posix(start_date)
    psoix_end_date = convert_to_posix(end_date)

    url = f"https://connect-eu.catapultsports.com/api/v6/activities?start_time={psoix_start_date}&end_time={psoix_end_date}"
    headers = {
        "accept": "application/json",
        "authorization": TOKEN
    }

    response = requests.get(url, headers=headers)
    activities = response.json()
    non_competition_activities = [activity for activity in activities if "wedstrijd" not in activity["tags"]]
    non_competition_activities_id = [non_competition_activity['id'] for non_competition_activity in non_competition_activities]
    return non_competition_activities_id

def fetch_activity_stats(competition_ids, competition=False):
    url = "https://connect-eu.catapultsports.com/api/v6/stats"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": TOKEN
    }

    data = {
        "filters": [
            {
                "name": "activity_id",
                "comparison": "=",
                "values": competition_ids
            }
        ],
        "parameters": [
            "total_duration",
            "total_distance",
            "velocity_band1_total_distance",
            "velocity_band2_total_distance",
            "velocity_band3_total_distance",
            "velocity_band4_total_distance",
            "velocity_band5_total_distance",
            "velocity_band6_total_distance",
        ],
        "group_by": [
            "athlete",
            "activity"
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    list_response = response.json()
    if competition == True:
        competitions_to_delete = []
        for competition in list_response:
            if competition['total_duration'] < 5250:
                competitions_to_delete.append(competition)
        
        for competition in competitions_to_delete:
            list_response.remove(competition)

    return list_response

def update_athlete_max(list_response, ofparameter=None, dbparameter=None):
    athlete_id = None
    total_distance = 0

    for data in list_response:
        if athlete_id == data['athlete_id']:
            athlete_id = data['athlete_id']
            if data[ofparameter] > total_distance:
                total_distance = data[ofparameter]
        else:
            if athlete_id is not None:  # Skip the update for the first iteration
                athlete = Athlete.objects.get(id=athlete_id)

                if getattr(athlete, dbparameter) < total_distance:
                    setattr(athlete, dbparameter, total_distance)
                    athlete.save()

            athlete_id = data['athlete_id']
            total_distance = data[ofparameter]

    if athlete_id is not None:
        athlete = Athlete.objects.get(id=athlete_id)
        if getattr(athlete, dbparameter) < total_distance:
            setattr(athlete, dbparameter, total_distance)
            athlete.save()

def update_athlete_average(list_response, ofparameter=None, dbparameter=None):
    athlete_id = None
    total_distance = 0
    count = 0

    for data in list_response:
        if athlete_id == data['athlete_id']:
            athlete_id = data['athlete_id']
            total_distance += data[ofparameter]
            count += 1
        else:
            if athlete_id is not None:  # Skip the update for the first iteration
                athlete = Athlete.objects.get(id=athlete_id)

                if count > 0:
                    average_distance = total_distance / count
                    setattr(athlete, dbparameter, average_distance)
                    athlete.save()

            athlete_id = data['athlete_id']
            total_distance = data[ofparameter]
            count = 1

    if athlete_id is not None:
        athlete = Athlete.objects.get(id=athlete_id)
        if count > 0:
            average_distance = total_distance / count
            setattr(athlete, dbparameter, average_distance)
            athlete.save()



def average(numbers):
    non_zero_numbers = [number for number in numbers if number != 0]

    if not non_zero_numbers:
        return None  # Return None for an empty list or a list with only zeros

    total = sum(non_zero_numbers)
    average = total / len(non_zero_numbers)
    return average


def update_athlete_cumulative_sum(list_response, ofparameter=None, dbparameter=None):
    athlete_id = None
    total_distance = 0
    count = 0


    for data in list_response:
        if athlete_id == data['athlete_id']:
            athlete_id = data['athlete_id']
            total_distance += data[ofparameter]
            count += 1
        else:
            if athlete_id is not None:  # Skip the update for the first iteration
                athlete = Athlete.objects.get(id=athlete_id)

                if count > 0:
                    setattr(athlete, dbparameter, total_distance)
                    athlete.save()

            athlete_id = data['athlete_id']
            total_distance = data[ofparameter]
            count = 1

    if athlete_id is not None:
        athlete = Athlete.objects.get(id=athlete_id)
        if count > 0:
            setattr(athlete, dbparameter, total_distance)
            athlete.save()


def update_temp_data(request):
    profile = request.user.profile

    start_date = str(profile.setting.start_date)
    end_date = str(profile.setting.end_date)

    print(end_date)

    activities = fetch_non_competition_activity_ids(start_date, end_date)
    print(len(activities))

    list_response = fetch_activity_stats(activities, competition=False)

    update_athlete_cumulative_sum(list_response, ofparameter='total_distance', dbparameter='temp_td')
    update_athlete_cumulative_sum(list_response, ofparameter='velocity_band1_total_distance', dbparameter='temp_walking')
    update_athlete_cumulative_sum(list_response, ofparameter='velocity_band2_total_distance', dbparameter='temp_jogging')
    update_athlete_cumulative_sum(list_response, ofparameter='velocity_band3_total_distance', dbparameter='temp_jogging2')
    update_athlete_cumulative_sum(list_response, ofparameter='velocity_band4_total_distance', dbparameter='temp_running')
    update_athlete_cumulative_sum(list_response, ofparameter='velocity_band5_total_distance', dbparameter='temp_HSR')
    update_athlete_cumulative_sum(list_response, ofparameter='velocity_band6_total_distance', dbparameter='temp_sprinting')



def safe_multiply(value, factor):
    if value is None:
        return None
    return value * factor