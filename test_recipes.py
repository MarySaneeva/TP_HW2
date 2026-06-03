import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe

def test_ingredient_creation():
    ing = Ingredient("Мука", 500.0, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"

def test_ingredient_str():
    ing = Ingredient("Мука", 500.0, "г")
    assert str(ing) == "Мука: 500.0 г"


def test_ingredient_eq():
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Мука", 300.0, "г")
    assert ing1 == ing2

    ing3 = Ingredient("Сахар", 500.0, "г")
    assert ing1 != ing3

    ing4 = Ingredient("Мука", 500.0, "кг")
    assert ing1 != ing4


def test_recipe_creation():
    ing1 = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Пицца", [ing1])
    assert recipe.title == "Пицца"
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Мука"


def test_recipe_add_ingredient():
    ing1 = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Пицца", [ing1])

    ing_same = Ingredient("Мука", 300.0, "г")
    recipe.add_ingredient(ing_same)
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 800.0

    ing_new = Ingredient("Вода", 200.0, "мл")
    recipe.add_ingredient(ing_new)
    assert len(recipe.ingredients) == 2


def test_recipe_scale():
    ing1 = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Пицца", [ing1])

    scaled_recipe = recipe.scale(2)
    assert scaled_recipe is not recipe
    assert scaled_recipe.ingredients[0].quantity == 1000.0

    assert recipe.ingredients[0].quantity == 500.0

    with pytest.raises(ValueError):
        recipe.scale(0)
    with pytest.raises(ValueError):
        recipe.scale(-1)


def test_recipe_len():
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Вода", 200.0, "мл")
    recipe = Recipe("Пицца", [ing1, ing2])
    assert len(recipe) == 2