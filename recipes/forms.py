from django import forms
from recipes.models import Recipe
from recipes.models import Food

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ["creation_date"]

class FoodIdForm(forms.Form):
    food_name = forms.CharField(label='Food name', max_length=200)