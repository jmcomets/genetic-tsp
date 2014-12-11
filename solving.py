import random
from functools import reduce

def random_solve(citymap, starting_city):
    cities = list(citymap.cities)
    cities.remove(starting_city)
    random.shuffle(cities)
    cities.insert(0, starting_city)
    return cities

def genetic_solve(citymap, starting_city):
    """Solve the TSP using a genetic algorithm."""
    cities = list(citymap.cities)
    cities.remove(starting_city)

    # helpers
    compute_distance = lambda c1, c2: citymap.distance_between(c1, c2)

    # parameters
    compute_fitness = lambda cs: sum(compute_distance(cs[i], cs[i+1])
                             for i in range(len(cs)-1))
    popsize = 100
    iterations = 100
    selection_popsize = int(popsize * .25)
    mutation_chance = .2

    # initial population
    population = [list(cities) for _ in range(popsize)]
    for genome in population:
        random.shuffle(genome)

    for i in range(iterations):
        print('iteration', i)

        # selection: roulette-wheel method
        new_population = []
        for _ in range(selection_popsize):
            # compute initial fitnesses
            genome_fitnesses = [(g, 1/compute_fitness(g)) for g in population]

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
        population = new_population

        # reproduction
        new_population = []
        while len(new_population) < popsize:
            # choose parents
            # TODO maybe two necessarily different parents ?
            first_parent = random.choice(population)
            second_parent = random.choice(population)

            # PMX cross-over (two opposite children)
            i, j = (random.randint(0, len(first_parent)) for _ in range(2))
            first_child = first_parent[:i] + second_parent[i:j] + first_parent[j+1:]
            second_child = second_parent[:i] + first_parent[i:j] + second_parent[j+1:]

            # mutation
            for child in (first_child, second_child):
                i, j = (random.randint(0, len(child)-1) for _ in range(2))
                child[i], child[j] = child[j], child[i]
            new_population.append(first_child)
            new_population.append(second_child)

    # return best candidate
    genome_fitnesses = ((g, compute_fitness(g)) for g in population)
    genome_fitnesses = sorted(genome_fitnesses, key=lambda gf: gf[1], reverse=True)
    return genome_fitnesses[0][0]

solve = random_solve
