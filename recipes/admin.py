from django.contrib import admin

from .models import FoodCategory, Food, Recipe, RecipeFood

admin.site.register(FoodCategory)
admin.site.register(Food)
admin.site.register(Recipe)
admin.site.register(RecipeFood)
