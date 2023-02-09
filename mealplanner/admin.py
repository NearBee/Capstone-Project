from django.contrib import admin
from mealplanner.models import (
    User,
    Pantry,
    Recipe,
    Ingredients,
    Planner,
    PlannerDay,
    Favorite,
)

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "date_joined")


admin.site.register(User, UserAdmin)


class PantryAdmin(admin.ModelAdmin):
    list_display = ("id", "ingredient_name")


admin.site.register(Pantry, PantryAdmin)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "recipe_name",
        "recipe_instructions",
        "nutritional_values",
        "dietary_preference",
    )


admin.site.register(Recipe, RecipeAdmin)


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ("id", "pantry_item", "recipe", "quantity")


admin.site.register(Ingredients, IngredientsAdmin)


class PlannerAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "is_private")


admin.site.register(Planner, PlannerAdmin)


class PlannerDayAdmin(admin.ModelAdmin):
    list_display = ("id", "day_of_week", "meal", "planner")


admin.site.register(PlannerDay, PlannerDayAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "planner")


admin.site.register(Favorite, FavoriteAdmin)
