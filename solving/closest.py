def solve(citymap, starting_city):
    cities = set(c for c in citymap.cities if c != starting_city)
    city = starting_city
    path = []
    while cities:
        next_city = min(cities, key=lambda c: citymap.distance_between(city, c))
        cities.remove(next_city)
        path.append(city)
        city = next_city
    path.append(next_city)
    return path
