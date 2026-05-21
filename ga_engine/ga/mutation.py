import random

from .chromosome import Genome


def mutate_random_reset(
    genome: Genome,
    rng: random.Random,
    guard_count: int,
    gene_mutation_rate: float = 0.02,
) -> Genome:
    mutated = genome[:]
    for idx in range(len(mutated)):
        if rng.random() < gene_mutation_rate:
            mutated[idx] = rng.randrange(guard_count)
    return mutated
