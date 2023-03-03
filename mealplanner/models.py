from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum, IntEnum

# Create your models here.


class User(AbstractUser):
    pass

    username = models.CharField(blank=False, unique=True, max_length=25)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(blank=False, max_length=128)
    favorite_dishes = models.ManyToManyField("Recipe", related_name="Fav_dishes")

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

    def __str__(self):
        return self.name

    def formatted_instructions(self):
        return self.instructions.replace("\n", "<br>")

    def formatted_nutrition(self):
        return self.nutritional_values.replace("\n", "<br>")


class Ingredient_List(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name="ingredient_details", on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, related_name="shopping_list", on_delete=models.CASCADE
    )
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.quantity} {self.ingredient.unit_of_measurement} {self.ingredient.name}"


class DaysOfWeek(Enum):
    SUNDAY = "Sunday"
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"


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
    days = models.IntegerField(
        choices=[(day.value, day.name) for day in NumberOfDays],
        default=1,
    )
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.owner} : Planner {self.pk} (Planner duration: {self.days} day(s))"
        )


class PlannerDay(models.Model):
    planner = models.ForeignKey(Planner, on_delete=models.CASCADE)
    meal = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    day_of_week = models.CharField(
        choices=[(day.name, day.value) for day in DaysOfWeek], max_length=10
    )
