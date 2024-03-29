from django.db import models
import pytz
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import truncatechars
from enum import Enum, IntEnum

# Create your models here.


class User(AbstractUser):
    pass

    TIMEZONES = tuple(zip(pytz.common_timezones, pytz.common_timezones))

    username = models.CharField(blank=False, unique=True, max_length=25)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(blank=False, max_length=128)
    timezone = models.CharField(max_length=100, choices=TIMEZONES, default="UTC")
    favorite_dishes = models.ManyToManyField("Recipe", related_name="Fav_dishes")
    profile_picture = models.ImageField(default="headshot_placeholder.png")

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
        ("Whole", "whole"),
        ("Pinch", "pinch"),
        ("Slice", "slice"),
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
    nopreference = "No Preference"
    vegetarian = "Vegetarian"
    vegan = "Vegan"
    pescetarian = "Pescetarian"
    dairyfree = "Dairy-Free"
    glutenfree = "Gluten-Free"


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, through="Ingredient_List")
    instructions = models.TextField()
    nutritional_values = models.TextField()
    dietary_preference = models.CharField(
        choices=[(diet.name, diet.value) for diet in Diets], max_length=14
    )
    recipe_photo = models.ImageField(default="Food_placeholder.jpg")
    recipe_description = models.TextField(
        default="Nothing Here",
    )

    def __str__(self):
        return self.name

    def formatted_instructions(self):
        return self.instructions.replace("\n", "<br>")

    def formatted_nutrition(self):
        return self.nutritional_values.replace("\n", "<br>")

    @property
    def short_instructions(self):
        return truncatechars(self.instructions, 50)

    @property
    def short_description(self):
        if not None:
            return truncatechars(self.recipe_description, 50)


class Ingredient_List(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name="ingredient_details", on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, related_name="shopping_list", on_delete=models.CASCADE
    )
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.quantity:.{0 if self.quantity.is_integer() else 2}f} {self.ingredient.unit_of_measurement} {self.ingredient.name}"


class NumberOfDays(IntEnum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7


class Planner(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=24, blank=False, null=True)
    days = models.IntegerField(
        choices=[(day.value, day.name) for day in NumberOfDays],
        default=1,
    )
    is_private = models.BooleanField(default=False)
    chosen_list = models.ManyToManyField(Recipe, related_name="chosen_dishes")
    not_saveable = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        User,
        related_name="user_likes",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner} : {self.name} (Planner duration: {self.days} day(s))"


class PlannerDay(models.Model):
    planner = models.ForeignKey(Planner, on_delete=models.CASCADE)
    meal = models.ManyToManyField(Recipe, related_name="boxes")
    day_number = models.IntegerField(null=True, blank=True)
