from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import user_registration_form, user_login_form
from .models import (
    User,
    Ingredient,
    Recipe,
    Ingredient_List,
    Planner,
    PlannerDay,
    DaysOfWeek,
)


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
        password2 = request.POST["password_confirmation"]
        if form["password"].value() != password2:
            message = "Passwords do not match"
            return render(
                request,
                "register.html",
                {"user_registration_form": user_registration_form, "message": message},
            )

        if form.is_valid():
            username = form["username"].value()
            email = form["email"].value()
            password = form["password"].value()
            User.objects.create_user(username, email, password)
            return redirect("index")

        else:
            message = "Sorry that username is unavailable"
            return render(
                request,
                "register.html",
                {"user_registration_form": user_registration_form, "message": message},
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
            message = "Username/Password is incorrect"
            return render(
                request,
                "login.html",
                {"user_login_form": user_login_form, "message": message},
            )

    else:
        return render(request, "login.html", {"user_login_form": user_login_form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def recipes_view(request):
    recipes = Recipe.objects.all()
    quantities = Ingredient_List.objects.all()
    user = request.user
    if user.is_authenticated:
        user_favorites = user.favorite_dishes.all()
        favorite_dishes = [recipe.name for recipe in user_favorites]

        return render(
            request,
            "recipes.html",
            {
                "recipes": recipes,
                "quantities": quantities,
                "favorite_dishes": favorite_dishes,
            },
        )

    return render(
        request,
        "recipes.html",
        {
            "recipes": recipes,
            "quantities": quantities,
        },
    )


@login_required
def favorite_recipe(request, id):
    user = request.user
    dish = Recipe.objects.get(id=id)

    if dish in user.favorite_dishes.all():
        user.favorite_dishes.remove(id)
    else:
        user.favorite_dishes.add(id)

    return redirect("recipes")
