from django.shortcuts import render
from django.http import HttpResponse
import copy
import logging
import json
import traceback
import datetime
from decimal import Decimal, ROUND_HALF_UP
from .forms import RecipeForm, FoodIdForm
from .models import Food, Recipe, RecipeFood

logger = logging.getLogger(__name__)

class RecipeView:         
        def __init__(self, recipe=None):
            if not recipe:
                self.id = 0
                self.name = ""
                self.description = ""
                self.properties = []
                return

            self.id = recipe.id
            self.name = recipe.recipe_name
            self.description = recipe.description
            self.foods = RecipeFood.objects.filter(recipe__pk=recipe.id)
            kcal = Decimal(0)
            carbs = Decimal(0)
            protein = Decimal(0)
            fat = Decimal(0)
            price = Decimal(0)
            pricePer1000Kcal = Decimal(0)
            percentProtein = Decimal(0)
            for recipeFood in self.foods:
                food = Food.objects.get(id=recipeFood.food.id)
                multOf100g = Decimal(recipeFood.quantity_grams) / 100
                kcal += food.kcal_per_100g * multOf100g
                carbs += food.carbs_per_100g * multOf100g
                protein += food.protein_per_100g * multOf100g
                fat += food.fat_per_100g * multOf100g
                price += food.cost_per_kg * multOf100g / 10

            pricePer1000Kcal = (price / (kcal / Decimal(1000))) if kcal else Decimal(0)
            percentProtein = (protein * 4 / (carbs * 4 + protein * 4 + fat * 4) * 100) if carbs or protein or fat else Decimal(0)

            kcal = kcal.quantize(Decimal('0.1'), ROUND_HALF_UP)
            carbs = carbs.quantize(Decimal('0.1'), ROUND_HALF_UP)
            protein = protein.quantize(Decimal('0.1'), ROUND_HALF_UP)
            fat = fat.quantize(Decimal('0.1'), ROUND_HALF_UP)
            price = price.quantize(Decimal('0.01'), ROUND_HALF_UP)
            pricePer1000Kcal = pricePer1000Kcal.quantize(Decimal('0.01'), ROUND_HALF_UP)
            percentProtein = percentProtein.quantize(Decimal('0.01'), ROUND_HALF_UP)

            currency = " zł"

            self.properties = []
            self.properties.extend([
                ('kcal', kcal),
                ('carbs', str(carbs) + 'g'),
                ('protein', str(protein) + 'g'),
                ('fat', str(fat) + 'g'),
                ('price', str(price) + currency),
                ('price per 1000 kcal', str(pricePer1000Kcal) + currency),
                ('% Protein', str(percentProtein) + "%")
            ])

        def __repr__(self):
            return self.name + str(self.properties)

# Create your views here.
def index(request):

    if request.POST:
        try:
            if request.POST["action"] == "delete":
                recipe = Recipe.objects.filter(id=int(request.POST['recipe_id']))
                recipe.delete()
        except:
            logger.error(traceback.format_exc())

    basket_props = {
        "name": "Basket",
        "kcal": 0,
        "carbs": 0,
        "protein": 0,
        "fat": 0,
        "price": 0,
        "price per 1000 kcal": 0,
        "% protein": 0
    }
    
    property_order = [
        "kcal", "carbs", "protein", "fat", "price", "price per 1000 kcal", "% protein"
    ]
    
    
        
    basket = RecipeView()
    basket.name = "Basket"
    for property in property_order:
        basket.properties.append((property, basket_props[property]))
       
    recipes = Recipe.objects.all()
    recipeViews = []
    for recipe in recipes:        
        recipeViews.append(RecipeView(recipe))

        
    return render(request, 'recipes/index.html', {"recipes": recipeViews, "basket": basket})

def updateRecipeFoods(recipeId, pickedFoods):
    # delete
    logger.debug(RecipeFood.objects.filter(recipe_id=recipeId))
    for recipeFood in RecipeFood.objects.filter(recipe_id=recipeId):
        if not str(recipeFood.food_id) in pickedFoods:
            logger.debug("I am going to delete food with id " + str(recipeFood.food_id))
            recipeFood.delete()

    # update/create
    for foodId, foodWeight in pickedFoods.items():
        recipeFoods = RecipeFood.objects.filter(food_id=int(foodId), recipe_id=int(recipeId))
        logger.debug(recipeFoods)
        if(recipeFoods):
            logger.debug("found existing food")
            if recipeFoods[0].quantity_grams != foodWeight:
                recipeFoods[0].quantity_grams = foodWeight
                recipeFoods[0].save()
            # delete duplicates
            for elem in recipeFoods[1:]:
                logger.debug("deleting a duplicate")
                elem.delete()
        else:
            logger.debug("creating new food")
            newRecipeFood = RecipeFood(food_id=foodId, recipe_id=recipeId, quantity_grams=foodWeight)
            newRecipeFood.save()

def new_recipe(request):    

    if request.POST:
        try:
            logger.debug(request.POST)
            newRecipe = Recipe(creation_date=datetime.datetime.now(), recipe_name=request.POST['recipe_name'], description=request.POST['description'])
            newRecipe.save()
            recipeId = newRecipe.id
            pickedFoods = json.loads(request.POST['picked_foods'])
            updateRecipeFoods(recipeId, pickedFoods)
        except:
            logger.debug(traceback.format_exc())

    return render(request, 'recipes/new-recipe.html', {
        "recipe_form": RecipeForm(), 
        "food_form": FoodIdForm(), 
        "foods": Food.objects.all()
        })

def recipe(request, recipe_id):
    if request.POST:
        try:
            logger.debug(request.POST)
            pickedFoods = json.loads(request.POST['picked_foods'])
            updateRecipeFoods(recipe_id, pickedFoods)
        except:
            logger.debug(traceback.format_exc())

    recipe = RecipeView(Recipe.objects.get(id=recipe_id))
    
    return render(request, "recipes/recipe.html", {
        "recipe": recipe,
        "foods": Food.objects.all()
    })
