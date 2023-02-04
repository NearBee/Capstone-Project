from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import user_creation_form, user_login_form
from .models import User


# Create your views here.


def index(request):
    return render(
        request,
        "index.html",
        {"user_creation_form": user_creation_form, "user_login_form": user_login_form},
    )


def register(request):
    if request.method == "POST":
        form = user_creation_form(request.POST)

        # Get two passwords for confirmation
        password2 = form["passwordconfirm"]
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
        else:
            return render(request, "index.html", {"message": ""})

    else:
        return render(request, "index.html", {"message": ""})


def login_view(request):
    if request.method == "POST":
        form = user_login_form(request.POST)

        # Attempt to sign user in
        email = form["email"]
        password = form["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "index.html", {"message": "Successfully logged in!"})

    else:
        return render(request, "index.html", {"message": ""})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
