import random

from .chromosome import Genome
from ..models.schedule_model import ShiftProblem


def create_individual(problem: ShiftProblem, rng: random.Random) -> Genome:
    return [rng.randrange(len(problem.guards)) for _ in range(problem.slot_count())]
