from typing import List, Tuple
import random

from .chromosome import Genome


def uniform_crossover(
    parent1: Genome,
    parent2: Genome,
    rng: random.Random,
) -> Tuple[Genome, Genome]:
    child1: List[int] = []
    child2: List[int] = []
    for gene1, gene2 in zip(parent1, parent2):
        if rng.random() < 0.5:
            child1.append(gene1)
            child2.append(gene2)
        else:
            child1.append(gene2)
            child2.append(gene1)
    return child1, child2
