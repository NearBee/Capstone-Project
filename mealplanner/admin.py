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
    list_display = ("id", "name")


admin.site.register(Ingredient, IngredientAdmin)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "instructions",
        "nutritional_values",
        "dietary_preference",
    )


admin.site.register(Recipe, RecipeAdmin)


class Ingredient_ListAdmin(admin.ModelAdmin):
    list_display = ("id", "recipe", "ingredient", "quantity")


admin.site.register(Ingredient_List, Ingredient_ListAdmin)


class PlannerAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "is_private")


admin.site.register(Planner, PlannerAdmin)


class PlannerDayAdmin(admin.ModelAdmin):
    list_display = ("id", "day_of_week", "meal", "planner")


admin.site.register(PlannerDay, PlannerDayAdmin)
