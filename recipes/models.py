from django.db import models

class FoodCategory(models.Model):
    category_name = models.CharField(max_length = 200)
    
class Food(models.Model):
    food_name = models.CharField(max_length = 200)
    cost_per_kg = models.DecimalField(decimal_places = 2, max_digits = 9)
    food_category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True, blank=True)
    kcal_per_100g = models.DecimalField(decimal_places = 1, max_digits = 5)
    carbs_per_100g = models.DecimalField(decimal_places = 1, max_digits = 4)
    protein_per_100g = models.DecimalField(decimal_places = 1, max_digits = 4)
    fat_per_100g = models.DecimalField(decimal_places = 1, max_digits = 4)

class Recipe(models.Model):
    recipe_name = models.CharField(max_length = 200)
    description = models.TextField()
    creation_date = models.DateTimeField()
    
class RecipeFood(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE)
    food = models.ForeignKey(Food, on_delete = models.PROTECT)
    quantity_grams = models.PositiveIntegerField()
    
