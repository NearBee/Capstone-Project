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
        password2 = form["password_confirmation"].value()
        if form["password"].value() != password2:
            # TODO: Should redirect to a register page
            return redirect("index")

        # POSSIBLE solution for register
        # return render(request, "register.html")

        if form.is_valid():
            username = form["username"].value()
            email = form["email"].value()
            password = form["password"].value()
            User.objects.create_user(username, email, password)
            return redirect("index")
        else:
            # TODO: Should redirect to a register page
            return redirect("index")

    # POSSIBLE solution for register
    # return render(request, "register.html", {"user_creation_form": user_creation_form})

    else:
        # TODO: Should redirect to a register page
        return redirect("index")

    # POSSIBLE solution for register
    # return render(request, "register.html", {"user_creation_form": user_creation_form})


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
            # Need more a clear error message for user not existing
            # TODO: Should redirect to a full page for logging in
            message = "User does not exist"
            # return redirect("index")

            # POSSIBLE solution for failed login
            return render(request, "login.html", {"user_login_form": user_login_form})

    else:
        print("Not Post")
        # return redirect("index")

        # POSSIBLE solution for failed login
        return render(request, "login.html", {"user_login_form": user_login_form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
