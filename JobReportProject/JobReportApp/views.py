from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required

from .models import User

# Create your views here.

def index(request):
    return render(request, "JobReportApp/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign the user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "JobReportApp/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "JobReportApp/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches password confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "JobReportApp/register.html", {
                "message": "Passwords must match."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "JobReportApp/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "JobReportApp/register.html")

def all_users_view(request):
    all_users = get_user_model().objects.all()
    context = {'allusers': all_users}
    return render(request, "JobReportApp/all-users.html", context)