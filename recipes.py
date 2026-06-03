class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value_float = float(value)
        if value_float <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value_float

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        if isinstance(other, Ingredient):
            return self.name == other.name and self.unit == other.unit
        return False

class Recipe:
    def __init__(self, title, ingredients):
        self.title = title
        self.ingredients = ingredients

    def add_ingredient(self, ingredient):
        for i in self.ingredients:
            if i == ingredient:
                i.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and not isinstance(ratio, bool) and ratio > 0

    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффициент масштабирования должен быть положительным числом")

        scale_ingredients = [Ingredient(ing.name, ing.quantity * ratio, ing.unit) for ing in self.ingredients]
        return Recipe(self.title, scale_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        ingredients_str = "\n".join([f" - {ing}" for ing in self.ingredients])
        return f"Рецепт: {self.title}\nИнгрeдиенты:\n{ingredients_str}"

class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)

        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title):
        self._items = [item for item in self._items if item[1] != title]

    def get_list(self):
        ingredients_dict = {}
        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)

            if key in ingredients_dict:
                ingredients_dict[key] += ingredient.quantity
            else:
                ingredients_dict[key] = ingredient.quantity
        result_list = [Ingredient(name, quantity, unit) for (name, unit), quantity in ingredients_dict.items()]
        result_list.sort(key=lambda x: x.name)
        return result_list

    def __add__(self, other):
        new_list = ShoppingList()
        new_list._items = self._items + other._items
        return new_list

class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        if ingredients is None:
            ingredients = []
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio):
        scaled_base_recipe = super().scale(ratio)
        return DietaryRecipe(scaled_base_recipe.title, self.diet_type, scaled_base_recipe.ingredients)

    def __str__(self):
        parent_str = super().__str__()
        return f"[{self.diet_type}] " + parent_str.replace("Рецепт: ", "")
