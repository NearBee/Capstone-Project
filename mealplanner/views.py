from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import user_creation_form, user_login_form
from .models import User


# Create your views here.


def index(request):
    return render(request, "index.html", {"user_registration_form": user_creation_form})


def register(request):
    if request.method == "POST":
        form = user_creation_form(request.POST)

        # Get two passwords for confirmation
        password2 = request.POST["passwordconfirm"]
        if form["password"] != password2:
            return render(request, "index.html", {"message": "Passwords must match."})

        if form.is_valid():
            username = form["username"]
            email = form["email"]
            password = form["password"]
            User.objects.create_user(username, email, password)
            return render(
                request, "index.html", {"message": "Successfully created account!"}
            )
