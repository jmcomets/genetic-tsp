import random

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

def crossover(parents):
    assert len(parents) == 2
    assert len(parents[0]) == len(parents[1])
    first, second = map(list, parents)
    a, b = 0, 0
    while not a < b:
        a, b = (random.randint(0, len(first)-1) for _ in range(2))
    for i in range(a, b+1):
        j = second.index(first[i])
        first[i], second[j] = second[j], first[i]
    return random.choice((first, second))

def mutation(child):
    assert len(child) > 1
    i, j = (random.randint(0, len(child)-1) for _ in range(2))
    child[i], child[j] = child[j], child[i]

def reproduction(population, popsize, crossover_p, mutation_p):
    nb_parents = 2
    nb_children = 2

    new_population = []
    while len(new_population) < popsize:
        # choose parents
        # TODO maybe two necessarily different parents ?
        parents = [random.choice(population) for _ in range(nb_parents)]

        # apply genetic operators
        for _ in range(nb_children):
            # PMX cross-over (two opposite children)
            if random.random() < crossover_p:
                child = crossover(parents)
            else:
                child = random.choice(parents)

            # mutation: swap two elements
            if random.random() < mutation_p:
                mutation(child)

            # add child to new population
            new_population.append(child)
    return new_population

def genetic_method(citymap, starting_city):
    """Solve the TSP using a genetic algorithm."""
    cities = list(citymap.cities)
    cities.remove(starting_city)

    # helpers
    compute_distance = lambda c1, c2: citymap.distance_between(c1, c2)
    compute_path_distance = lambda cs: sum(compute_distance(cs[i], cs[i+1])
                                           for i in range(len(cs)-1))

    # parameters
    popsize = 80
    iterations = 200
    selection_proportion = .2
    crossover_p = .3
    mutation_p = .05
    fitness_f = lambda cs: 1/compute_path_distance(cs)

    # run genetic algorithm
    steps = []
    population = initialize_population(cities, popsize)
    for i in range(iterations):
        population = selection(population, fitness_f,
                               int(popsize * selection_proportion))
        population = reproduction(population, popsize, crossover_p, mutation_p)

        # yield best genome
        genome_distances = ((g, compute_path_distance(g)) for g in population)
        genome_distances = sorted(genome_distances, key=lambda gf: gf[1])
        steps.append((i,) + genome_distances[0])
    return steps, steps[-1][1]
