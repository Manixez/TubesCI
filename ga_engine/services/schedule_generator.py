from typing import List

from ..models.input_model import InputModel
from ..models.result_model import ScheduleRow
from ..models.schedule_model import ShiftProblem
from ..ga.chromosome import Genome


def build_problem(input_model: InputModel) -> ShiftProblem:
    return ShiftProblem(
        buildings=input_model.buildings,
        guards=input_model.guards,
        shifts=input_model.normalized_shifts(),
        days=input_model.normalized_days(),
        guards_per_shift=input_model.guards_per_shift,
        min_days_off=input_model.min_days_off,
    )


def decode_schedule(genome: Genome, problem: ShiftProblem) -> List[List[List[List[int]]]]:
    n_days = len(problem.days)
    n_buildings = len(problem.buildings)
    n_shifts = len(problem.shifts)
    guards_per_shift = problem.guards_per_shift

    schedule = [
        [[[] for _ in range(n_shifts)] for _ in range(n_buildings)]
        for _ in range(n_days)
    ]

    idx = 0
    for day_idx in range(n_days):
        for building_idx in range(n_buildings):
            for shift_idx in range(n_shifts):
                guards = []
                for _ in range(guards_per_shift):
                    guards.append(genome[idx])
                    idx += 1
                schedule[day_idx][building_idx][shift_idx] = guards

    return schedule


def schedule_rows(
    schedule: List[List[List[List[int]]]],
    problem: ShiftProblem,
) -> List[ScheduleRow]:
    rows: List[ScheduleRow] = []
    for day_idx, day_name in enumerate(problem.days):
        for building_idx, building_name in enumerate(problem.buildings):
            for shift_idx, shift_name in enumerate(problem.shifts):
                guard_names = [problem.guards[g] for g in schedule[day_idx][building_idx][shift_idx]]
                rows.append(
                    ScheduleRow(
                        day=day_name,
                        building=building_name,
                        shift=shift_name,
                        guards=guard_names,
                    )
                )
    return rows
