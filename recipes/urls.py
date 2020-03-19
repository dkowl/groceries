from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new-recipe', views.new_recipe, name='new-recipe'),
    path('<int:recipe_id>', views.recipe)
]