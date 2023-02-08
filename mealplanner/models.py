from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

# Create your models here.


class User(AbstractUser):
    pass

    username = models.CharField(blank=False, unique=True, max_length=25)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(blank=False, max_length=128)
    password_confirmation = models.CharField(blank=False, max_length=128)

    def __str__(self):
        return self.username


class Pantry(models.Model):
    ingredient_name = models.CharField(max_length=100)
    # TODO: look at calculating ingredients rather than storing in pantry


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=100)
    recipe_ingredients = models.ManyToManyField(Pantry, through="Ingredients")
    recipe_instructions = models.TextField()
    nutritional_values = models.TextField()
    dietary_preference = models.CharField(max_length=100)


class Ingredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    pantry_item = models.ForeignKey(Pantry, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)


class DaysOfWeek(Enum):
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


class Planner(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    days = models.ManyToManyField(Recipe, through="PlannerDay")
    is_private = models.BooleanField(default=False)


class PlannerDay(models.Model):
    planner = models.ForeignKey(Planner, on_delete=models.CASCADE)
    meal = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    day_of_week = models.CharField(
        choices=[(day.name, day.value) for day in DaysOfWeek], max_length=10
    )


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    planner = models.ForeignKey(Planner, on_delete=models.CASCADE)
