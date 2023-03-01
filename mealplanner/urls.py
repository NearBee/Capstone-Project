from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("recipes", views.recipes_view, name="recipes"),
    path("favorite/<int:id>", views.favorite_recipe, name="fav_recipe"),
    path("", views.add_planner, name="add_planner"),
]
