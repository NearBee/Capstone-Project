from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

# Create your models here.


class User(AbstractUser):
    pass

    username = models.CharField(blank=False, unique=True, max_length=25)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(blank=False, max_length=128)

    def __str__(self):
        return self.username


class Ingredient(models.Model):
    MEASURES = [
        ("Millilitres", "millilitres"),
        ("Litres", "litres"),
        ("Grams", "grams"),
        ("Kilograms", "kilograms"),
        ("Teaspoons", "teaspoon"),
        ("Tablespoons", "tablespoon"),
        ("Cups", "cup"),
        ("Ounces", "ounce"),
        ("Pints", "pint"),
        ("Pounds", "pound"),
        ("Quantity", "quantity"),
    ]
    name = models.CharField(max_length=100)
    unit_of_measurement = models.CharField(
        choices=MEASURES,
        max_length=128,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} ({self.unit_of_measurement})"


class Diets(Enum):
    Vegetarian = "Vegetarian"
    Vegan = "Vegan"
    Pescetarian = "Pescetarian"
    DairyFree = "Dairy-Free"
    GlutenFree = "Gluten-Free"


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, through="Ingredient_List")
    instructions = models.TextField()
    nutritional_values = models.TextField()
    dietary_preference = models.CharField(
        choices=[(diet.name, diet.value) for diet in Diets], max_length=14
    )

    # TODO: Add a Textfield for Ingredients that could be parsed for a shopping list

    def __str__(self):
        return self.name

    def formatted_instructions(self):
        return self.instructions.replace("\n", "<br>")

    def formatted_nutrition(self):
        return self.nutritional_values.replace("\n", "<br>")


class Ingredient_List(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.recipe} - {self.ingredient.name} {self.quantity} {self.ingredient.unit_of_measurement}"


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
