class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    def quantity(self, value):
        value_float = float(value)
        if value_float <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value_float

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eg__(self, other):
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
        return f"Рецепт: {self.title}\nИнгридиенты:\n{ingredients_str}"