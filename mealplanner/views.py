import datetime

import pytz
import tinify  # type: ignore
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from typing import Callable, Any

from .forms import (
    planner_creation_form,
    user_edit_form,
    user_login_form,
    user_registration_form,
)
from .models import Ingredient_List, Planner, Recipe, User


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to time a function.

    Args:
        func (Callable[..., Any]): Function to be timed.
    """

    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        result = func(*args, **kwargs)
        end = datetime.datetime.now()
        print(f"Time taken: {end - start}")
        return result

    return wrapper


def index(request: Any) -> Any:
    """Index page view.

    Args:
        request (GET): GET request to index page.

    Returns:
        HttpResponse: Renders index page with quanities for use in profile information.
    """

    user = request.user
    recipes = Recipe.objects.all()
    quantities = Ingredient_List.objects.all()

    if not user.is_authenticated:
        return render(
            request,
            "index.html",
            {
                "recipes": recipes,
                "quantities": quantities,
            },
        )

    user_favorites = user.favorite_dishes.all()
    favorite_dishes = [recipe.name for recipe in user_favorites]

    return render(
        request,
        "index.html",
        {
            "recipes": recipes,
            "quantities": quantities,
            "favorite_dishes": favorite_dishes,
        },
    )


def register(request: HttpRequest) -> HttpResponse:
    """Register page view.

    Args:
        request (POST): POST request to register page.

    Returns:
        HttpResponse: Submits a form to register a new user and redirects to index page.
    """

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
    """Login page view.

    Args:
        request (POST): POST request to login page.

    Returns:
        HttpResponse: Submits a form to login a user and redirects to index page.
    """

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
    """Logout page view.

    Args:
        request (GET): GET request to logout page.

    Returns:
        HttpResponse: Logs out user and redirects to index page.
    """

    logout(request)
    return HttpResponseRedirect(reverse("index"))


@timer
@login_required(redirect_field_name="", login_url="login")
def edit_profile(request, id):
    """Edit profile page view.

    Args:
        request (POST): POST request to edit profile page through AJAX.
        id (int): ID of user.

    Returns:
        JsonResponse: Returns JSON response with user information.

        If the form is not valid it returns a JSON response with the id and a message regarding the error.

        The submission of the form will also be sent to the Tinify API for optimization,
        if the limit of images optimized this month is exceeded the image will not be optimized.
    """

    user = request.user
    form = user_edit_form(request.POST, request.FILES, instance=user)

    if not form.is_valid():
        return JsonResponse({"id": id, "message": "Form is not valid"}, status=400)

    form.save()

    # Try to send the image to tinify API to optimize it
    try:
        # If successful the image will come back optimized and will be set as the new image
        updated_image = tinify.from_file(user.profile_picture.path)  # type: ignore
        updated_image.to_file(user.profile_picture.path)

    except tinify.AccountError:
        # If the limit of images optimized this month is exceeded the image will not be optimized
        print(
            "Unfortunately exceeded the limit of images optimized this month, the image is still used but is not optimized, please try again next month"
        )

    return JsonResponse(
        {
            "username": user.username,
            "email": user.email,
            "profile_picture": user.profile_picture.url,
        },
        status=200,
    )


def recipes_view(request):
    """Recipes page view.

    Args:
        request (GET): GET request to recipes page.

    Returns:
        HttpResponse: Renders recipes page with recipes and quantities.
        Also shows the current athenticated user's favorite recipes.
    """

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
    """View for favoring a recipe.

    Args:
        request (POST): Post request to favorite a recipe using AJAX.
        id (int): ID of recipe.

    Returns:
        JsonResponse: Returns JSON response with id of recipe.

        if the recipe is already within the authenticated user's favorites the function will instead remove the favorite
    """

    user = request.user
    dish = Recipe.objects.get(id=id)

    if dish in user.favorite_dishes.all():
        user.favorite_dishes.remove(id)
    else:
        user.favorite_dishes.add(id)

    return JsonResponse({"id": id}, status=200)


@login_required(redirect_field_name="", login_url="login")
def create_planner(request):
    """View for creating a planner.

    Args:
        request (POST): Post request using the planner_creation_form to create a planner.

    Returns:
        HttpResponse: Renders the index page with the planner_creation_form.
    """

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
    """View for adding a recipe to the planner.

    Args:
        request (POST): Post request to add a recipe to the planner using AJAX.
        id (int): ID of recipe.

    Returns:
        JsonResponse: Returns JSON response with recipe information.

        If the planner.not_saveable == True and the planner.chosen_list.count() != planner.days
        not_saveable is then changed to False for the option to add more recipes to the planner.

        If the planner.not_saveable == False and the planner.chosen_list.count() < planner.days
        then the recipe is added to the planner.
    """

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
    """View for removing a recipe from the planner.

    Args:
        request (POST): Post request to remove a recipe from the planner using AJAX.
        id (int): ID of recipe.

    Returns:
        JsonResponse: Returns JSON response with recipe information.

        If the recipe is in the planner's chosen list then it is removed.
    """

    user = request.user
    planner = Planner.objects.filter(owner=user).latest("id")
    recipe = get_object_or_404(Recipe, id=id)

    if recipe in planner.chosen_list.all():
        planner.chosen_list.remove(recipe)
        return JsonResponse({"success": True, "id": recipe.pk}, status=200)

    return JsonResponse({"success": False, "id": recipe.pk}, status=400)


@login_required(redirect_field_name="", login_url="login")
def finalize_planner(request, id):
    """View for finalizing the planner.

    Args:
        request (POST): Post request to finalize the planner using AJAX.
        id (int): ID of planner.

    Returns:
        HttpResponse: After the planner is finalized the user is redirected to the planner page.
    """

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
    """View for the planner page.

    Args:
        request (GET): Get request to render the planner page.

    Returns:
        HttpResponse: Renders the planner page with all the planners and the active planner.

        If the user currently has an "active planner" then the active planner is rendered at the top of the page.
    """

    user = request.user
    planners = Planner.objects.all().filter(finished=True)

    if not user.is_authenticated:
        return render(request, "planner_page.html", {"planners": planners})

    active_planner = Planner.objects.filter(owner=user).latest("id")
    created_date = datetime.datetime.now().date() - active_planner.created_at.date()
    print(abs(created_date.days))

    if not abs(created_date.days) >= active_planner.days:
        return render(
            request,
            "planner_page.html",
            {
                "planners": planners,
                "active_planner": active_planner,
            },
        )

    return render(request, "planner_page.html", {"planners": planners})


@login_required(redirect_field_name="", login_url="login")
def like_planner(request, id):
    """View for liking a planner.

    Args:
        request (POST): Post request to like a planner using AJAX.
        id (int): ID of planner.

    Returns:
        JsonResponse: Returns JSON response with message.

        If the user has already liked the planner then the user is removed from the planner's likes.
        Else the user is added to the planner's likes.
    """

    planner = Planner.objects.get(id=id)

    if not request.method == "POST":
        return JsonResponse({"error": "Something went wrong"}, status=404)

    if request.user in planner.likes.all():
        planner.likes.remove(request.user)
    else:
        planner.likes.add(request.user)

    return JsonResponse({"message": "Planner liked!"}, status=200)


def get_likes(request, id):
    """View for getting the number of likes a planner has.

    Args:
        request (GET): Get request to get the number of likes a planner has using AJAX.
        id (int): ID of planner.

    Returns:
        JsonResponse: Returns JSON response with the number of likes of the target_planner.
    """

    target_planner = Planner.objects.get(id=id)
    return JsonResponse({"likes": target_planner.likes.count()})


@login_required(redirect_field_name="", login_url="login")
def add_to_cart(request, id):
    """View for adding the planner's chosen list to the shopping list.

    Args:
        request (POST): Request to add the planner's chosen list to the shopping list using AJAX.
        id (int): id of planner.

    Returns:
        JsonResponse: Returns JSON response with message and shopping list.

        The planner's chosen list is added to the shopping list.
    """

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
    """View for editing a planner.

    Args:
        request (POST): Post request to edit a planner using AJAX.
        id (int): id of planner.

    Returns:
        HttpReponse: After the planner is edited the user is redirected to the planner page.

        If the user != the planner.owner they are presented with a copy of the planner with the chosen dishes.

        If the user == the planner.owner they are presented with a version of the planner where th finished flag is set to False.
    """

    user = request.user
    planner = Planner.objects.get(id=id)
    old_planner_dishes = planner.chosen_list.all()

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
