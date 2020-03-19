from django.db import models

class FoodCategory(models.Model):
    category_name = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.category_name
    
class Food(models.Model):
    food_name = models.CharField(max_length = 200)
    cost_per_kg = models.DecimalField(decimal_places = 2, max_digits = 9)
    food_category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True, blank=True)
    kcal_per_100g = models.DecimalField(decimal_places = 1, max_digits = 5)
    carbs_per_100g = models.DecimalField(decimal_places = 1, max_digits = 4)
    protein_per_100g = models.DecimalField(decimal_places = 1, max_digits = 4)
    fat_per_100g = models.DecimalField(decimal_places = 1, max_digits = 4)
    
    def __str__(self):
        return self.food_name

class Recipe(models.Model):
    recipe_name = models.CharField(max_length = 200)
    description = models.TextField()
    creation_date = models.DateTimeField()
    
    def __str__(self):
        return self.recipe_name
    
class RecipeFood(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE)
    food = models.ForeignKey(Food, on_delete = models.PROTECT)
    quantity_grams = models.PositiveIntegerField()
    
    def __str__(self):
        return "{0} ({1}) - {2} ({3})".format(self.recipe.recipe_name, self.recipe.id, self.food.food_name, self.food.id)
    
