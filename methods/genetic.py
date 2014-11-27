import random

def solve(citymap, starting_city):
    cities = list(citymap.cities)
    cities.remove(starting_city)
    random.shuffle(cities)
    cities.insert(0, starting_city)
    return cities
