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


def test_shopping_list_add_recipe():
    ing = Ingredient("Мука", 500.0, "г")
    recipe = Recipe("Пицца", [ing])
    shop_list = ShoppingList()

    shop_list.add_recipe(recipe, 2)
    items = shop_list.get_list()
    assert len(items) == 1
    assert items[0].name == "Мука"
    assert items[0].quantity == 1000.0

    with pytest.raises(ValueError):
        shop_list.add_recipe(recipe, 0)


def test_shopping_list_remove_recipe():
    ing1 = Ingredient("Мука", 500.0, "г")
    recipe1 = Recipe("Пицца", [ing1])
    ing2 = Ingredient("Мясо", 300.0, "г")
    recipe2 = Recipe("Борщ", [ing2])

    shop_list = ShoppingList()
    shop_list.add_recipe(recipe1, 1)
    shop_list.add_recipe(recipe2, 1)

    shop_list.remove_recipe("Пицца")
    items = shop_list.get_list()
    assert len(items) == 1
    assert items[0].name == "Мясо"


def test_shopping_list_aggregation_and_sorting():
    ing1 = Ingredient("Мука", 500.0, "г")
    recipe1 = Recipe("Пицца", [ing1])
    ing2 = Ingredient("Мука", 200.0, "г")
    ing3 = Ingredient("Вода", 100.0, "мл")
    recipe2 = Recipe("Хлеб", [ing2, ing3])

    shop_list = ShoppingList()
    shop_list.add_recipe(recipe1, 1)
    shop_list.add_recipe(recipe2, 1)

    items = shop_list.get_list()
    assert len(items) == 2
    assert items[0].name == "Вода"
    assert items[1].name == "Мука"
    assert items[1].quantity == 700.0  # 500 + 200


def test_shopping_list_add_operator():
    ing1 = Ingredient("Мука", 500.0, "г")
    recipe1 = Recipe("Пицца", [ing1])
    shop_list1 = ShoppingList()
    shop_list1.add_recipe(recipe1, 1)

    ing2 = Ingredient("Сахар", 100.0, "г")
    recipe2 = Recipe("Чай", [ing2])
    shop_list2 = ShoppingList()
    shop_list2.add_recipe(recipe2, 1)

    combined_list = shop_list1 + shop_list2
    items = combined_list.get_list()

    assert len(items) == 2