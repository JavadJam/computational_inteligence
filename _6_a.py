import random


def fitness(cand):
    x, y, z = cand
    return (4 * (x**2)) + (0.5 * (z**2)) + ((x**3) / (y**2)) + (x * y)


def gen_cand():
    x = random.uniform(1, 50)
    y = random.uniform(1/3, 3/2)
    z = random.uniform(x/4, x)
    return (x, y, z)


def choose(pop):
    sorted_pop = sorted(pop, key=fitness)

    n = len(sorted_pop)
    ranks = list(range(n, 0, -1))
    sum_ranks = sum(ranks)
    probs = [r / sum_ranks for r in ranks]

    return random.choices(sorted_pop, weights=probs, k=1)[0]


def cross(p1, p2):
    w = random.random()
    child = []

    for i in range(len(p1)):
        child.append(w * p1[i] + (1 - w) * p2[i])

    return child


def mutate(cand, prob=0.5):
    x, y, z = cand

    if random.random() < prob:
        gene = random.randint(0, 2)

        if gene == 0:
            x = random.uniform(1, 50)

        elif gene == 1:
            y = random.uniform(1/3, 3/2)

        else:
            z = random.uniform(x/4, x)

    return (x, y, z)


def genetic(pop_size=200, gens=400, elite_percent=10, patience=15, imig_percent=30):

    elite_size = int(pop_size * (elite_percent / 100))

    pop = [gen_cand() for _ in range(pop_size)]

    best_fitness = float("inf")
    stagnation = 0

    for gen in range(gens):

        pop = sorted(pop, key=fitness)
        best_cand = pop[0]
        current_best = fitness(best_cand)

        #check improvements
        if current_best < best_fitness:
            best_fitness = current_best
            stagnation = 0
        else:
            stagnation += 1

        next_pop = pop[:elite_size]

        while len(next_pop) < pop_size:
            p1 = choose(pop)
            p2 = choose(pop)

            child = cross(p1, p2)
            child = mutate(child)

            next_pop.append(child)

        pop = next_pop

        #preven stagnation
        if stagnation >= patience:
            imigs = int(pop_size * (imig_percent / 100))
            pop[-imigs:] = [gen_cand() for _ in range(imigs)]
            stagnation = 0

        if gen % 10 == 0:
            print("gen", gen, ": best =", best_cand, "fitness =", current_best)

    return best_cand



result = genetic()
print("\nfinal result =", result, "fitness =", fitness(result))