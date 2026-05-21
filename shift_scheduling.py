from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import math
import random

DEFAULT_DAYS = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat",
    "Sabtu",
    "Minggu",
]
DEFAULT_SHIFTS = ["Shift 1", "Shift 2"]


@dataclass
class ShiftProblem:
    buildings: List[str]
    guards: List[str]
    guards_per_shift: int
    min_days_off: int = 0
    days: List[str] = field(default_factory=lambda: DEFAULT_DAYS[:])
    shifts: List[str] = field(default_factory=lambda: DEFAULT_SHIFTS[:])

    def slot_count(self) -> int:
        return (
            len(self.days)
            * len(self.buildings)
            * len(self.shifts)
            * self.guards_per_shift
        )


@dataclass
class PenaltyWeights:
    missing_guard: float = 200.0
    double_shift_day: float = 80.0
    day_off_shortage: float = 40.0
    workload_balance: float = 10.0
    building_repeat: float = 3.0


@dataclass
class ScheduleMetrics:
    missing_guards: int
    double_shift_days: int
    day_off_shortage: int
    workload_stdev: float
    building_repeat_excess: float
    total_penalty: float


def create_individual(problem: ShiftProblem, rng: random.Random) -> List[int]:
    return [rng.randrange(len(problem.guards)) for _ in range(problem.slot_count())]


def uniform_crossover(
    parent1: List[int],
    parent2: List[int],
    rng: random.Random,
) -> Tuple[List[int], List[int]]:
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


def mutate_random_reset(
    genome: List[int],
    rng: random.Random,
    guard_count: int,
    gene_mutation_rate: float = 0.02,
) -> List[int]:
    mutated = genome[:]
    for i in range(len(mutated)):
        if rng.random() < gene_mutation_rate:
            mutated[i] = rng.randrange(guard_count)
    return mutated


def decode_schedule(genome: List[int], problem: ShiftProblem) -> List[List[List[List[int]]]]:
    n_days = len(problem.days)
    n_buildings = len(problem.buildings)
    n_shifts = len(problem.shifts)
    guards_per_shift = problem.guards_per_shift

    schedule = [
        [[[] for _ in range(n_shifts)] for _ in range(n_buildings)]
        for _ in range(n_days)
    ]

    idx = 0
    for d in range(n_days):
        for b in range(n_buildings):
            for s in range(n_shifts):
                guards = []
                for _ in range(guards_per_shift):
                    guards.append(genome[idx])
                    idx += 1
                schedule[d][b][s] = guards

    return schedule


def evaluate_schedule(
    genome: List[int],
    problem: ShiftProblem,
    weights: PenaltyWeights,
) -> Tuple[float, ScheduleMetrics]:
    schedule = decode_schedule(genome, problem)
    n_guards = len(problem.guards)
    n_days = len(problem.days)
    n_shifts = len(problem.shifts)
    n_buildings = len(problem.buildings)
    guards_per_shift = problem.guards_per_shift

    guard_shift_presence = [
        [[False for _ in range(n_shifts)] for _ in range(n_days)]
        for _ in range(n_guards)
    ]
    guard_day_presence = [[False for _ in range(n_days)] for _ in range(n_guards)]
    guard_building_counts = [
        [0 for _ in range(n_buildings)] for _ in range(n_guards)
    ]

    missing_guards = 0

    for d in range(n_days):
        for b in range(n_buildings):
            for s in range(n_shifts):
                guards = schedule[d][b][s]
                unique_guards = set(guards)
                if len(unique_guards) < guards_per_shift:
                    missing_guards += guards_per_shift - len(unique_guards)

                for g in guards:
                    guard_building_counts[g][b] += 1
                    guard_shift_presence[g][d][s] = True
                    guard_day_presence[g][d] = True

    guard_shift_counts = [0 for _ in range(n_guards)]
    double_shift_days = 0

    for g in range(n_guards):
        for d in range(n_days):
            shifts_worked = sum(1 for s in range(n_shifts) if guard_shift_presence[g][d][s])
            if shifts_worked > 1:
                double_shift_days += 1
        guard_shift_counts[g] = sum(
            1
            for d in range(n_days)
            for s in range(n_shifts)
            if guard_shift_presence[g][d][s]
        )

    day_off_shortage = 0
    for g in range(n_guards):
        days_worked = sum(1 for d in range(n_days) if guard_day_presence[g][d])
        days_off = n_days - days_worked
        if days_off < problem.min_days_off:
            day_off_shortage += problem.min_days_off - days_off

    avg_shifts = sum(guard_shift_counts) / max(1, n_guards)
    variance = (
        sum((count - avg_shifts) ** 2 for count in guard_shift_counts) / max(1, n_guards)
    )
    workload_stdev = math.sqrt(variance)

    building_repeat_excess = 0.0
    for g in range(n_guards):
        total_assignments = sum(guard_building_counts[g])
        if total_assignments == 0:
            continue
        avg_per_building = total_assignments / max(1, n_buildings)
        max_on_one_building = max(guard_building_counts[g])
        excess = max(0.0, max_on_one_building - (avg_per_building + 1.0))
        building_repeat_excess += excess

    total_penalty = (
        weights.missing_guard * missing_guards
        + weights.double_shift_day * double_shift_days
        + weights.day_off_shortage * day_off_shortage
        + weights.workload_balance * workload_stdev
        + weights.building_repeat * building_repeat_excess
    )

    metrics = ScheduleMetrics(
        missing_guards=missing_guards,
        double_shift_days=double_shift_days,
        day_off_shortage=day_off_shortage,
        workload_stdev=workload_stdev,
        building_repeat_excess=building_repeat_excess,
        total_penalty=total_penalty,
    )

    return total_penalty, metrics


def schedule_rows(
    schedule: List[List[List[List[int]]]],
    problem: ShiftProblem,
) -> List[List[str]]:
    rows: List[List[str]] = []
    for d, day_name in enumerate(problem.days):
        for b, building_name in enumerate(problem.buildings):
            for s, shift_name in enumerate(problem.shifts):
                guard_names = [problem.guards[g] for g in schedule[d][b][s]]
                rows.append([day_name, building_name, shift_name] + guard_names)
    return rows


def summarize_guards(
    schedule: List[List[List[List[int]]]],
    problem: ShiftProblem,
) -> List[Dict[str, str]]:
    n_guards = len(problem.guards)
    n_days = len(problem.days)
    n_shifts = len(problem.shifts)
    n_buildings = len(problem.buildings)

    guard_shift_presence = [
        [[False for _ in range(n_shifts)] for _ in range(n_days)]
        for _ in range(n_guards)
    ]
    guard_building_presence = [
        [False for _ in range(n_buildings)] for _ in range(n_guards)
    ]

    for d in range(n_days):
        for b in range(n_buildings):
            for s in range(n_shifts):
                for g in schedule[d][b][s]:
                    guard_shift_presence[g][d][s] = True
                    guard_building_presence[g][b] = True

    guard_shift_counts = [
        sum(
            1
            for d in range(n_days)
            for s in range(n_shifts)
            if guard_shift_presence[g][d][s]
        )
        for g in range(n_guards)
    ]

    avg_shifts = sum(guard_shift_counts) / max(1, n_guards)
    summaries: List[Dict[str, str]] = []

    for g in range(n_guards):
        if guard_shift_counts[g] > avg_shifts + 1:
            label = "Beban cukup tinggi"
        elif guard_shift_counts[g] < avg_shifts - 1:
            label = "Beban rendah"
        else:
            label = "Beban normal"

        buildings = [
            problem.buildings[b]
            for b in range(n_buildings)
            if guard_building_presence[g][b]
        ]

        summaries.append(
            {
                "name": problem.guards[g],
                "total_shifts": str(guard_shift_counts[g]),
                "buildings": ", ".join(buildings) if buildings else "-",
                "label": label,
            }
        )

    return summaries
