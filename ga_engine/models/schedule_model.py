from dataclasses import dataclass
from typing import List


@dataclass
class ShiftProblem:
    buildings: List[str]
    guards: List[str]
    shifts: List[str]
    days: List[str]
    guards_per_shift: int
    min_days_off: int = 0

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
    overlap_shift: float = 120.0
    day_off_shortage: float = 40.0
    workload_balance: float = 10.0
    building_repeat: float = 3.0


@dataclass
class ScheduleMetrics:
    missing_guards: int
    double_shift_days: int
    overlap_shift_assignments: int
    day_off_shortage: int
    workload_stdev: float
    building_repeat_excess: float
    total_penalty: float
