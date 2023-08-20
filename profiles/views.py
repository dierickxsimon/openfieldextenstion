from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate ,logout
from django.shortcuts import render, redirect
from .models import Profile, Setting, User
from .forms import SettingForm
from utils.utils import update_temp_data


# Create your views here.

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('getplots')
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        
        except:
            messages.error(request, 'username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None: 
            login(request, user) #login function is going to create a session in the session table in the db and it's going to give this to the browsers cookies 
            return redirect(request.GET['next'] if 'next' in request.GET else 'getplots')
        
        else:
            messages.error(request, 'username OR password is incorrect')

    return render(request, 'profiles/login_registr.html') 

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('login')


@login_required(login_url='login')
def updateSetting(request): 
    profile = request.user.profile
    setting = profile.setting
    form = SettingForm(instance=setting)
    if request.method == 'POST':
        setting_form = SettingForm(request.POST, instance=setting)
        if setting_form.is_valid():
            setting_form.save()
            update_temp_data(request)
            return redirect('getplots')
        
        

        
        else:
            messages.error(request, f'Oops something went wrong')

    context = {'form':form}
    return render(request, 'profiles/setting.html', context)

    
