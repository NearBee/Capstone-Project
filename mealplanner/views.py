from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import user_registration_form, user_login_form
from .models import User


def index(request):
    return render(
        request,
        "index.html",
        {
            "user_registration_form": user_registration_form,
            "user_login_form": user_login_form,
        },
    )


def register(request):
    if request.method == "POST":
        form = user_registration_form(request.POST)

        # Get two passwords for confirmation
        password2 = form["password_confirmation"].value()
        if form["password"].value() != password2:
            return render(
                request,
                "register.html",
                {"user_registration_form": user_registration_form},
            )

        if form.is_valid():
            username = form["username"].value()
            email = form["email"].value()
            password = form["password"].value()
            User.objects.create_user(username, email, password)
            return redirect("index")
        else:
            return render(
                request,
                "register.html",
                {"user_registration_form": user_registration_form},
            )

    else:
        return render(
            request, "register.html", {"user_registration_form": user_registration_form}
        )


def login_view(request):
    if request.method == "POST":
        form = user_login_form(request.POST)

        # Attempt to sign user in
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            message = "User does not exist"
            return render(request, "login.html", {"user_login_form": user_login_form})

    else:
        return render(request, "login.html", {"user_login_form": user_login_form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
