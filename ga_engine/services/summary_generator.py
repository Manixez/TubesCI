from typing import List

from ..models.result_model import GuardSummary
from ..models.schedule_model import ShiftProblem


def summarize_guards(
    schedule: List[List[List[List[int]]]],
    problem: ShiftProblem,
) -> List[GuardSummary]:
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

    for day_idx in range(n_days):
        for building_idx in range(n_buildings):
            for shift_idx in range(n_shifts):
                for guard_idx in schedule[day_idx][building_idx][shift_idx]:
                    guard_shift_presence[guard_idx][day_idx][shift_idx] = True
                    guard_building_presence[guard_idx][building_idx] = True

    guard_shift_counts = [
        sum(
            1
            for day_idx in range(n_days)
            for shift_idx in range(n_shifts)
            if guard_shift_presence[guard_idx][day_idx][shift_idx]
        )
        for guard_idx in range(n_guards)
    ]

    avg_shifts = sum(guard_shift_counts) / max(1, n_guards)
    summaries: List[GuardSummary] = []

    for guard_idx in range(n_guards):
        if guard_shift_counts[guard_idx] > avg_shifts + 1:
            label = "Beban cukup tinggi"
        elif guard_shift_counts[guard_idx] < avg_shifts - 1:
            label = "Beban rendah"
        else:
            label = "Beban normal"

        buildings = [
            problem.buildings[b]
            for b in range(n_buildings)
            if guard_building_presence[guard_idx][b]
        ]

        summaries.append(
            GuardSummary(
                name=problem.guards[guard_idx],
                total_shifts=guard_shift_counts[guard_idx],
                buildings=buildings,
                label=label,
            )
        )

    return summaries
