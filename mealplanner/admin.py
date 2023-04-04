from django.contrib import admin
from mealplanner.models import (
    User,
    Ingredient,
    Recipe,
    Ingredient_List,
    Planner,
    PlannerDay,
)

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "date_joined")


admin.site.register(User, UserAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "unit_of_measurement")


admin.site.register(Ingredient, IngredientAdmin)


class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "short_instructions",
        "nutritional_values",
        "dietary_preference",
        "short_description",
        "recipe_photo",
    ]


admin.site.register(Recipe, RecipeAdmin)


class Ingredient_ListAdmin(admin.ModelAdmin):
    list_display = ("id", "recipe", "ingredient", "quantity")


admin.site.register(Ingredient_List, Ingredient_ListAdmin)


class PlannerAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "is_private")


admin.site.register(Planner, PlannerAdmin)


class PlannerDayAdmin(admin.ModelAdmin):
    list_display = ("id", "day_number", "planner")


admin.site.register(PlannerDay, PlannerDayAdmin)
