import random
from functools import reduce

__all__ = ('genetic_method',)

def initialize_population(cities, popsize):
    population = [list(cities) for _ in range(popsize)]
    for genome in population:
        random.shuffle(genome)
    return population

def selection(population, fitness_f, popsize):
    # selection: roulette-wheel method
    new_population = []
    for _ in range(popsize):
        # compute initial fitnesses
        genome_fitnesses = [(g, fitness_f(g)) for g in population
                            if g not in new_population]

        # normalize fitnesses
        total_fs = sum(f for _, f in genome_fitnesses)
        genome_fitnesses = ((g, f/total_fs) for g, f in genome_fitnesses)

        # accumulate fitnesses
        genome_fitnesses = sorted(genome_fitnesses, key=lambda gf: gf[1], reverse=True)
        genome_fitnesses = [(gf[0], gf[1]/sum(f for _, f in genome_fitnesses[:i+1]))
                            for i, gf in enumerate(genome_fitnesses)]

        # select first genome with fitness gt a random number from [0, 1)
        rn = random.random()
        for genome, fitness in genome_fitnesses:
            if fitness > rn:
                selected_genome = genome
                break
        new_population.append(selected_genome)
    return new_population

def reproduction(population, popsize):
    # reproduction
    new_population = []
    while len(new_population) < popsize:
        # choose parents
        # TODO maybe two necessarily different parents ?
        first = random.choice(population)
        second = random.choice(population)

        # PMX cross-over (two opposite children)
        a, b = 0, 0
        while not a < b:
            a, b = (random.randint(0, len(first)-1) for _ in range(2))
        for i in range(a, b+1):
            j = second.index(first[i])
            first[i], second[j] = second[j], first[i]

        # mutation: swap two elements
        for child in (first, second):
            i, j = (random.randint(0, len(child)-1) for _ in range(2))
            child[i], child[j] = child[j], child[i]
        new_population.append(first)
        new_population.append(second)
    return new_population

def genetic_method(citymap, starting_city):
    """Solve the TSP using a genetic algorithm."""
    cities = list(citymap.cities)
    cities.remove(starting_city)

    # helpers
    compute_distance = lambda c1, c2: citymap.distance_between(c1, c2)

    # parameters
    popsize = 50
    iterations = 500
    selection_proportion = .2
    mutation_chance = .2
    compute_fitness = lambda cs: 1/sum(compute_distance(cs[i], cs[i+1])
                                       for i in range(len(cs)-1))

    # run genetic algorithm
    population = initialize_population(cities, popsize)
    for _ in range(iterations):
        population = selection(population, compute_fitness,
                               int(popsize * selection_proportion))
        population = reproduction(population, popsize)

    # return best candidate
    genome_fitnesses = ((g, compute_fitness(g)) for g in population)
    genome_fitnesses = sorted(genome_fitnesses, key=lambda gf: gf[1], reverse=True)
    return genome_fitnesses[0][0]
