from django.shortcuts import render
from django.shortcuts import redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from userprofile.models import Profile

# Create your views here.

def register(request):
    if request.method == "POST":
        form =RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            new_profile=Profile(user=user)
            new_profile.save()
            login(request, user)
            
        return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form":form})