from typing import Tuple
import math

from .chromosome import Genome
from ..models.schedule_model import PenaltyWeights, ScheduleMetrics, ShiftProblem
from ..services.schedule_generator import decode_schedule


def evaluate_schedule(
    genome: Genome,
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
    guard_day_shift_counts = [
        [[0 for _ in range(n_shifts)] for _ in range(n_days)]
        for _ in range(n_guards)
    ]

    missing_guards = 0

    for day_idx in range(n_days):
        for building_idx in range(n_buildings):
            for shift_idx in range(n_shifts):
                guards = schedule[day_idx][building_idx][shift_idx]
                unique_guards = set(guards)
                if len(unique_guards) < guards_per_shift:
                    missing_guards += guards_per_shift - len(unique_guards)

                for guard_idx in guards:
                    guard_building_counts[guard_idx][building_idx] += 1
                    guard_shift_presence[guard_idx][day_idx][shift_idx] = True
                    guard_day_presence[guard_idx][day_idx] = True
                    guard_day_shift_counts[guard_idx][day_idx][shift_idx] += 1

    guard_shift_counts = [0 for _ in range(n_guards)]
    double_shift_days = 0

    for guard_idx in range(n_guards):
        for day_idx in range(n_days):
            shifts_worked = sum(
                1
                for shift_idx in range(n_shifts)
                if guard_shift_presence[guard_idx][day_idx][shift_idx]
            )
            if shifts_worked > 1:
                double_shift_days += 1
        guard_shift_counts[guard_idx] = sum(
            1
            for day_idx in range(n_days)
            for shift_idx in range(n_shifts)
            if guard_shift_presence[guard_idx][day_idx][shift_idx]
        )

    day_off_shortage = 0
    for guard_idx in range(n_guards):
        days_worked = sum(1 for day_idx in range(n_days) if guard_day_presence[guard_idx][day_idx])
        days_off = n_days - days_worked
        if days_off < problem.min_days_off:
            day_off_shortage += problem.min_days_off - days_off

    overlap_shift_assignments = 0
    for guard_idx in range(n_guards):
        for day_idx in range(n_days):
            for shift_idx in range(n_shifts):
                count = guard_day_shift_counts[guard_idx][day_idx][shift_idx]
                if count > 1:
                    overlap_shift_assignments += count - 1

    avg_shifts = sum(guard_shift_counts) / max(1, n_guards)
    variance = (
        sum((count - avg_shifts) ** 2 for count in guard_shift_counts) / max(1, n_guards)
    )
    workload_stdev = math.sqrt(variance)

    building_repeat_excess = 0.0
    for guard_idx in range(n_guards):
        total_assignments = sum(guard_building_counts[guard_idx])
        if total_assignments == 0:
            continue
        avg_per_building = total_assignments / max(1, n_buildings)
        max_on_one_building = max(guard_building_counts[guard_idx])
        excess = max(0.0, max_on_one_building - (avg_per_building + 1.0))
        building_repeat_excess += excess

    total_penalty = (
        weights.missing_guard * missing_guards
        + weights.double_shift_day * double_shift_days
        + weights.overlap_shift * overlap_shift_assignments
        + weights.day_off_shortage * day_off_shortage
        + weights.workload_balance * workload_stdev
        + weights.building_repeat * building_repeat_excess
    )

    metrics = ScheduleMetrics(
        missing_guards=missing_guards,
        double_shift_days=double_shift_days,
        overlap_shift_assignments=overlap_shift_assignments,
        day_off_shortage=day_off_shortage,
        workload_stdev=workload_stdev,
        building_repeat_excess=building_repeat_excess,
        total_penalty=total_penalty,
    )

    return total_penalty, metrics
