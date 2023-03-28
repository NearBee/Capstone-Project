import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import (
    planner_creation_form,
    user_edit_form,
    user_login_form,
    user_registration_form,
)
from .models import (
    Ingredient,
    Ingredient_List,
    Planner,
    PlannerDay,
    Recipe,
    User,
)


def index(request):
    user = request.user

    if not user.is_authenticated:
        return render(
            request,
            "index.html",
        )

    return render(
        request,
        "index.html",
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
            user = User.objects.create_user(username, email, password)  # type: ignore
            login(request, user)
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


@login_required(redirect_field_name="", login_url="login")
def edit_profile(request, id):
    user = request.user

    if not request.method == "POST":
        return JsonResponse({"id": id, "message": "Wasn't a Post"}, status=400)

    form = user_edit_form(request.POST, request.FILES, instance=user)

    if not form.is_valid():
        return JsonResponse({"id": id, "message": "Form is not valid"}, status=400)

    form.save()

    return JsonResponse(
        {
            "username": user.username,
            "email": user.email,
            "profile_picture": user.profile_picture.url,
        },
        status=200,
    )


def recipes_view(request):
    recipes = Recipe.objects.all()
    quantities = Ingredient_List.objects.all()
    user = request.user

    if not user.is_authenticated:
        return render(
            request,
            "recipes.html",
            {
                "recipes": recipes,
                "quantities": quantities,
            },
        )

    user_favorites = user.favorite_dishes.all()
    favorite_dishes = [recipe.name for recipe in user_favorites]

    if Planner.objects.filter(owner=user).count() == 0:
        return render(
            request,
            "recipes.html",
            {
                "recipes": recipes,
                "quantities": quantities,
                "favorite_dishes": favorite_dishes,
            },
        )

    planner = Planner.objects.filter(owner=user).latest("id")
    if planner.chosen_list.count() > 0:
        remainder = planner.days - planner.chosen_list.count()
        return render(
            request,
            "recipes.html",
            {
                "recipes": recipes,
                "quantities": quantities,
                "favorite_dishes": favorite_dishes,
                "planner": planner,
                "chosen_list": planner.chosen_list.all(),
                "remainder": remainder,
            },
        )

    return render(
        request,
        "recipes.html",
        {
            "recipes": recipes,
            "quantities": quantities,
            "favorite_dishes": favorite_dishes,
            "planner": planner,
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

    # TODO: Change from a redirect to a JSONresponse to save a reload
    return JsonResponse({"id": id}, status=200)


@login_required(redirect_field_name="", login_url="login")
def add_planner(request):
    user = request.user
    if request.method == "POST":
        planner_form = planner_creation_form(request.POST)
        print(planner_form.errors)
        if planner_form.is_valid():
            # planner is saved
            created_planner = planner_form.save(commit=False)
            created_planner.owner = user
            created_planner.save()
            return redirect("recipes")

    return render(request, "index.html", {"planner_form": planner_creation_form()})


def add_to_planner(request, id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=id)

    if not user.is_authenticated:
        return redirect("login")

    planner = Planner.objects.filter(owner=user).latest("id")

    # This is used incase the user wants to make edits to the planner
    if planner.not_saveable == True and planner.chosen_list.count() != planner.days:
        planner.not_saveable = False
        planner.save(update_fields=["not_saveable"])

        return JsonResponse(
            {
                "photo": recipe.recipe_photo,
                "name": recipe.name,
                "id": recipe.pk,
            },
            status=200,
        )

    # Add a recipe to the planner's chosen list
    if planner.not_saveable == False and planner.chosen_list.count() < planner.days:
        planner.chosen_list.add(recipe)

    return JsonResponse(
        {
            "photo": recipe.recipe_photo.url,
            "name": recipe.name,
            "id": recipe.pk,
        },
        status=200,
    )


@login_required(redirect_field_name="", login_url="login")
def remove_from_planner(request, id):
    user = request.user

    planner = Planner.objects.filter(owner=user).latest("id")
    recipe = get_object_or_404(Recipe, id=id)

    if recipe in planner.chosen_list.all():
        planner.chosen_list.remove(recipe)

    return JsonResponse({"id": recipe.pk}, status=200)


@login_required(redirect_field_name="", login_url="login")
def finalize_planner(request, id):
    user = request.user
    planner = get_object_or_404(Planner, id=id)

    # Finalize the planner
    if planner.chosen_list.count() >= planner.days:
        planner.finished = True
    planner.not_saveable = True
    planner.save(update_fields=["not_saveable", "finished"])

    if not request.method == "POST":
        return JsonResponse({"error": "Something went wrong"}, status=404)

    return redirect("planner_page")


def planner_page_view(request):
    user = request.user
    planners = Planner.objects.all().filter(finished=True)

    if not user.is_authenticated:
        return render(request, "planner_page.html", {"planners": planners})

    return render(request, "planner_page.html", {"planners": planners})


@login_required(redirect_field_name="", login_url="login")
def like_planner(request, id):
    planner = Planner.objects.get(id=id)
    if not request.user.is_authenticated:
        return redirect("login")

    if not request.method == "POST":
        return JsonResponse({"error": "Something went wrong"}, status=404)

    if request.user in planner.likes.all():
        planner.likes.remove(request.user)
    else:
        planner.likes.add(request.user)

    return JsonResponse({"message": "Planner liked!"}, status=200)


def get_likes(request, id):
    target_planner = Planner.objects.get(id=id)
    return JsonResponse({"likes": target_planner.likes.count()})


@login_required(redirect_field_name="", login_url="login")
def add_to_cart(request, id):
    planner = Planner.objects.get(id=id)
    shopping_list = {}

    if not request.method == "POST":
        return JsonResponse({"error": "Something went wrong"}, status=404)

    for recipe in planner.chosen_list.all():
        for ingredient in recipe.ingredient_details.filter(recipe=recipe):
            name = ingredient.ingredient.name
            quantity = ingredient.quantity
            unit_of_measurement = ingredient.ingredient.unit_of_measurement

            if name in shopping_list:
                # The item is already on the Shopping List
                shopping_list[name][0] += quantity

            # The item is not already in the shopping list
            shopping_list[name] = [
                quantity,
                unit_of_measurement,
            ]

    return JsonResponse(
        {
            "message": f"Planner: {planner.name} ingredients added to cart!",
            "shopping_list": shopping_list,
        },
        status=200,
    )


@login_required(redirect_field_name="", login_url="login")
def edit_planner(request, id):
    user = request.user
    planner = Planner.objects.get(id=id)
    old_planner_dishes = planner.chosen_list.all()

    if not user.is_authenticated:
        return redirect("login")

    if not user == planner.owner:
        planner.pk = None
        planner.owner = User.objects.get(id=user.id)
        planner.not_saveable = False
        planner.finished = False
        planner.save()
        planner.chosen_list.set(old_planner_dishes)

    planner.not_saveable = False
    planner.finished = False
    planner.save()
    planner.chosen_list.set(old_planner_dishes)

    return redirect("recipes")


def calendar_view(request):
    return render(request, "calendar.html")
