from dataclasses import dataclass
from typing import Callable, List, Tuple
import random

from .chromosome import Genome
from .selection import tournament_select

FitnessFn = Callable[[Genome], float]
CreateFn = Callable[[random.Random], Genome]
CrossoverFn = Callable[[Genome, Genome, random.Random], Tuple[Genome, Genome]]
MutateFn = Callable[[Genome, random.Random], Genome]


@dataclass
class GAConfig:
    population_size: int = 120
    generations: int = 200
    tournament_size: int = 3
    crossover_rate: float = 0.9
    mutation_rate: float = 0.3
    elite_count: int = 2
    seed: int = 12042026


@dataclass
class GAResult:
    best_genome: Genome
    best_fitness: float
    history: List[float]


def run_ga(
    config: GAConfig,
    create_individual: CreateFn,
    fitness_fn: FitnessFn,
    crossover_fn: CrossoverFn,
    mutate_fn: MutateFn,
) -> GAResult:
    rng = random.Random(config.seed)
    population = [create_individual(rng) for _ in range(config.population_size)]

    best_genome: Genome = population[0][:]
    best_fitness = float("inf")
    history: List[float] = []

    for _ in range(config.generations):
        scored = [(ind, fitness_fn(ind)) for ind in population]
        scored.sort(key=lambda item: item[1])

        if scored[0][1] < best_fitness:
            best_genome = scored[0][0][:]
            best_fitness = scored[0][1]

        history.append(scored[0][1])

        new_population = [chrom[:] for chrom, _ in scored[: config.elite_count]]
        while len(new_population) < config.population_size:
            parent1 = tournament_select(scored, config.tournament_size, rng)
            parent2 = tournament_select(scored, config.tournament_size, rng)

            if rng.random() < config.crossover_rate:
                child1, child2 = crossover_fn(parent1, parent2, rng)
            else:
                child1, child2 = parent1[:], parent2[:]

            if rng.random() < config.mutation_rate:
                child1 = mutate_fn(child1, rng)
            if rng.random() < config.mutation_rate:
                child2 = mutate_fn(child2, rng)

            new_population.append(child1)
            if len(new_population) < config.population_size:
                new_population.append(child2)

        population = new_population

    return GAResult(best_genome=best_genome, best_fitness=best_fitness, history=history)
