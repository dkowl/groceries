# Generated by Django 3.0.4 on 2020-03-15 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=200)),
                ('cost_per_kg', models.DecimalField(decimal_places=2, max_digits=9)),
                ('kcal_per_100g', models.DecimalField(decimal_places=1, max_digits=5)),
                ('carbs_per_100g', models.DecimalField(decimal_places=1, max_digits=4)),
                ('protein_per_100g', models.DecimalField(decimal_places=1, max_digits=4)),
                ('fat_per_100g', models.DecimalField(decimal_places=1, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('creation_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RecipeFood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_grams', models.PositiveIntegerField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recipes.Food')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='food',
            name='food_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.FoodCategory'),
        ),
    ]
