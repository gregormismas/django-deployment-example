from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required




# Create your views here.

def index(request):
    return render(request, "basic_app/index.html")

@login_required
def special(request):
    return HttpResponse("You are logged in, nice!")

@login_required
def user_logout(request):
    logout(request) # logs out the user
    return HttpResponseRedirect(reverse("index")) # reverses them to the index page

def register(request):
    registered = False
    
    if request.method == "POST": # checks for POST request
        user_form = UserForm(data=request.POST) # defines rendered forms
        profile_form = UserProfileInfoForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            
            user = user_form.save()
            user.set_password(user.password) # hashing the password
            user.save()
            
            profile = profile_form.save(commit=False) # don't save data right away, we need to make some modifications to data 
            profile.user = user # sets up the one to one relationship
            
            if "profile_pic" in request.FILES: # checks if a picture (file) has been posted, also used with other files
                profile.profile_pic = request.FILES["profile_pic"] # key defined in models.py
                
            profile.save()
            registered = True
        
        else:
            print(user_form.errors, profile_form.errors)
    else: 
        user_form = UserForm
        profile_form = UserProfileInfoForm
        
    return render(request, "basic_app/registration.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "registered": registered
    })
    
    
def user_login(request):
    
    if request.method == "POST": # if the user has filled out the form and pressed "Login"
        username = request.POST.get("username") # name "username" is sent via post from login.html form
        print("Username: {}".format(username))
        password = request.POST.get("password") # same for password
        
        user = authenticate(username=username, password=password) # builtin authentication, is passed to the html
        
        if user: # django checks if user is authenticated
            if user.is_active: # check if the user is active (can get inactivated if they spend too much time off website)
                login(request, user) # django logs in the user 
                return HttpResponseRedirect(reverse("index")) # it redirects them back to the homepage
            
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE") # tells the user they are not active
        else: 
            print("Someone tried to login and failed.") # if user fails to login
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")    
    else: 
        return render(request, "basic_app/login.html", {})
            