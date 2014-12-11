import random

def random_method(citymap, starting_city):
    cities = list(citymap.cities)
    cities.remove(starting_city)
    random.shuffle(cities)
    cities.insert(0, starting_city)
    return cities

from .genetic import genetic_method

solve = genetic_method
