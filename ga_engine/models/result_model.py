from dataclasses import dataclass
from typing import Any, Dict, List

from .schedule_model import ScheduleMetrics


@dataclass
class ScheduleRow:
    day: str
    building: str
    shift: str
    guards: List[str]


@dataclass
class GuardSummary:
    name: str
    total_shifts: int
    buildings: List[str]
    label: str


@dataclass
class ResultModel:
    schedule: List[ScheduleRow]
    guard_summary: List[GuardSummary]
    warnings: List[str]
    fitness_score: float
    metrics: ScheduleMetrics

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schedule": [
                {
                    "day": row.day,
                    "building": row.building,
                    "shift": row.shift,
                    "guards": row.guards,
                }
                for row in self.schedule
            ],
            "guardSummary": [
                {
                    "name": summary.name,
                    "totalShifts": summary.total_shifts,
                    "buildings": summary.buildings,
                    "label": summary.label,
                }
                for summary in self.guard_summary
            ],
            "warnings": self.warnings,
            "fitnessScore": self.fitness_score,
            "metrics": {
                "missingGuards": self.metrics.missing_guards,
                "doubleShiftDays": self.metrics.double_shift_days,
                "dayOffShortage": self.metrics.day_off_shortage,
                "workloadStdev": self.metrics.workload_stdev,
                "buildingRepeatExcess": self.metrics.building_repeat_excess,
                "totalPenalty": self.metrics.total_penalty,
            },
        }
