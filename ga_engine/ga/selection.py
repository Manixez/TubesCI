from typing import List, Tuple
import random

from .chromosome import Genome


def tournament_select(
    scored: List[Tuple[Genome, float]],
    tournament_size: int,
    rng: random.Random,
) -> Genome:
    candidates = rng.sample(scored, tournament_size)
    winner = min(candidates, key=lambda item: item[1])
    return winner[0][:]
