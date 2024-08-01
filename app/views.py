from django.shortcuts import render
import requests
from datetime import datetime
import math
from django.conf import settings
import pyrebase
from django.contrib import auth


SECRET_KEY = settings.SECRET_KEY
def index(request):
    def get_season():
        month = datetime.now().month
        if 4 <= month <= 6:
            return "spring"
        elif 7 <= month <= 9:
            return "summer"
        elif 10 <= month <= 12:
            return "fall"
        else:
            return "winter"

    current_year = datetime.now().year

    headers = {'X-MAL-CLIENT-ID': SECRET_KEY}
    response = requests.get(f'https://api.myanimelist.net/v2/anime/season/{current_year}/{get_season()}?sort=anime_num_list_users&fields=mean&limit=100', headers=headers)
    
    if response.status_code == 200:
        airing_now_data = response.json()
    else:
        print(f"Error: {response.status_code}")
    
    response = requests.get(f'https://api.myanimelist.net/v2/anime/ranking?fields=mean&limit=100', headers=headers)
    
    if response.status_code == 200:
        top_anime_data = response.json()
    else:
        print(f"Error: {response.status_code}")
    
    response = requests.get(f'https://api.myanimelist.net/v2/anime/ranking?ranking_type=bypopularity&fields=mean&limit=100', headers=headers)
    
    if response.status_code == 200:
        popular_anime_data = response.json()
    else:
        print(f"Error: {response.status_code}")
    
    response = requests.get(f'https://api.myanimelist.net/v2/anime/ranking?ranking_type=movie&fields=mean&limit=100', headers=headers)
    
    if response.status_code == 200:
        anime_movie = response.json()
    else:
        print(f"Error: {response.status_code}")
        
    context = {
        'airing_now_data': airing_now_data,
        'top_anime_data': top_anime_data,
        'popular_anime_data': popular_anime_data,
        'anime_movie': anime_movie
        }
    return render(request, 'index.html', context)
    

def index_two(request, anime_id):
    headers = {'X-MAL-CLIENT-ID': SECRET_KEY}
    response = requests.get(f'https://api.myanimelist.net/v2/anime/{anime_id}?fields=alternative_titles,pictures,start_date,end_date,synopsis,mean,rank,popularity,media_type,status,genres,rating,average_episode_duration,studios,related_anime,num_episodes,source,start_season,num_scoring_users', headers=headers)
    
    if response.status_code == 200:
        anime_data = response.json()
    else:
        print(f"Error: {response.status_code}")
    
    try:
        media_types = {
        "unknown": "Unknown",
        "tv": "TV",
        "ova": "OVA",
        "movie": "Movie",
        "special": "Special",
        "ona": "ONA",
        "music": "Music"
        } 
        media_type = media_types.get(anime_data['media_type'], "N/A")
    except:
        media_type = "N/A"
    
    try:
        season = anime_data["start_season"]["season"].replace('_', ' ').title()
    except:
        season = "N/A"
    
    try:
        episode_duration = math.floor(anime_data["average_episode_duration"]/60)
    except:
        episode_duration = "N/A"
        
    try:
        status = anime_data["status"].replace('_', ' ').title()
    except:
        status = "N/A"
        
    try:
        source = anime_data["source"].replace('_', ' ').title()
    except:
        source = "N/A"
    
    try:
        episodes = anime_data["num_episodes"]
    except:
        episodes = "N/A"
          
    try:
        ratings = {
        "g": "G - All Ages",
        "pg": "PG - Children",
        "pg_13": "PG-13 - Teens 13 and Older",
        "r": "R - 17+ (violence & profanity)",
        "r+": "R+ - Profanity & Mild Nudity"
        } 
        rating = ratings.get(anime_data['rating'], "N/A")
    except:
        rating = "N/A"
    
    context = {
        'anime_data': anime_data,
        'relation_length': len(anime_data['related_anime']),
        'media_type': media_type,
        'episode_duration': episode_duration,
        'episodes': episodes,
        'status': status,
        'source': source,
        'season': season,
        'rating': rating,
    }
    try:
        idToken = request.session['uid']
        user= fireAuth.get_account_info(idToken)
        name = database.child("users").child(user).child("details").child("name").get()
    except:
        return render(request, 'anime-view.html', context)
    return render(request, 'anime-view.html', context,{"name":name})

def index_three(request, search_query):
    from django.http import JsonResponse
    headers = {'X-MAL-CLIENT-ID': SECRET_KEY}
    response = requests.get(f'https://api.myanimelist.net/v2/anime?q={search_query}&fields=mean,media_type,num_episodes,start_date,end_date', headers=headers)
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        print(f"Error: {response.status_code}")

def login(request):
    return render(request,'account/login.html')

def signup(request):
    return render(request,'account/signup.html')


firebaseConfig = {
 "add you config":"here like this"
}
firebase = pyrebase.initialize_app(firebaseConfig)
fireAuth = firebase.auth()
database = firebase.database()     

def postSignIn(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = fireAuth.sign_in_with_email_and_password(email,password)
    except:
        message = "invalid cred"
        return render(request,'account/login.html',{"message":message})
    session_id = user['idToken']
    request.session['uid']=str(session_id)
    return index(request)

def logout(request):
    auth.logout
    return index(request)


def postSignUp(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = fireAuth.create_user_with_email_and_password(email,password)
        uid = user['localId']
        data= {"name":name,"status":"1","date":datetime.now()}
        database.child("users").child(uid).child("details").set(data)
        fireAuth.send_email_verification(user['idToken'])
    except:
        message = user
        return render(request,'account/signup.html',{"message":message})

