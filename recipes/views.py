from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
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
    
    class RecipeView:
        name = ""
        properties = []
        
    basket = RecipeView()
    basket.name = "Basket"
    for property in property_order:
        basket.properties.append((property, basket_props[property]))
       
    recipes = []
    recipes.append(basket)
    recipes.append(basket)
        
    return render(request, 'recipes/index.html', {"recipes": recipes, "basket": basket})
