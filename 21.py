# https://adventofcode.com/2020/day/21
import sys


input = [line.strip() for line in sys.stdin]


# part 1
ingredients_per_allergens = {}
all_ingredients = []
for food in input:
    ingredients, allergens = food.split(' (contains ')
    ingredients = ingredients.split()
    allergens = allergens.rstrip(')').split(', ')
    all_ingredients += ingredients
    for allergen in allergens:
        if allergen in ingredients_per_allergens:
            ingredients_per_allergens[allergen] &= set(ingredients)
        else:
            ingredients_per_allergens[allergen] = set(ingredients)

allergen_in_ingredient = {}
while len(allergen_in_ingredient) != len(ingredients_per_allergens):
    for allergen in ingredients_per_allergens:
        ingredient = list(ingredients_per_allergens[allergen])
        if len(ingredient) == 1 and ingredient[0] not in allergen_in_ingredient:
            allergen_in_ingredient[ingredient[0]] = allergen
            for allergen2 in ingredients_per_allergens:
                ingredients_per_allergens[allergen2] -= set(ingredient)


print(sum(1 for ingredient in all_ingredients if ingredient not in allergen_in_ingredient))

# part 2
print(','.join(sorted(list(allergen_in_ingredient), key=lambda x: allergen_in_ingredient[x])))
