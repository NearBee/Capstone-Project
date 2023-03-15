from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("recipes", views.recipes_view, name="recipes"),
    path("recipes/add_planner", views.add_planner, name="add_planner"),
    path("favorite/<int:id>", views.favorite_recipe, name="fav_recipe"),
    path(
        "recipes/add_to_planner/<int:id>", views.add_to_planner, name="add_to_planner"
    ),
    path(
        "recipes/remove_from_planner/<int:id>)",
        views.remove_from_planner,
        name="remove_from_planner",
    ),
    path(
        "finalize_planner/<int:id>",
        views.finalize_planner,
        name="finalize_planner",
    ),
    path("planners", views.planner_page_view, name="planner_page"),
    path("like_planner/<int:id>", views.like_planner, name="like_planner"),
    path("get_likes/<int:id>", views.get_likes, name="get_likes"),
    path("add_to_cart/<int:id>", views.add_to_cart, name="add_to_cart"),
    path("calendar", views.calendar_view, name="calendar"),
]
