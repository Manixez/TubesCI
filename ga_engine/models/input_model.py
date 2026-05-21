from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

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
class InputModel:
    buildings: List[str]
    guards: List[str]
    shifts: List[str] = field(default_factory=lambda: DEFAULT_SHIFTS[:])
    period_days: int = 7
    guards_per_shift: int = 1
    min_days_off: int = 0
    days: Optional[List[str]] = None
    ga: Optional[Dict[str, Any]] = None

    @staticmethod
    def from_dict(payload: Dict[str, Any]) -> "InputModel":
        buildings = payload.get("buildings") or []
        guards = payload.get("guards") or []

        shifts_payload = payload.get("shifts")
        shifts = shifts_payload if shifts_payload else DEFAULT_SHIFTS[:]

        period_days = int(payload.get("periodDays", payload.get("period_days", 7)) or 7)
        guards_per_shift = int(
            payload.get("guardsPerShift", payload.get("guards_per_shift", 1)) or 1
        )
        min_days_off = int(payload.get("minDaysOff", payload.get("min_days_off", 0)) or 0)
        days = payload.get("days")
        ga = payload.get("ga")

        return InputModel(
            buildings=buildings,
            guards=guards,
            shifts=shifts,
            period_days=period_days,
            guards_per_shift=guards_per_shift,
            min_days_off=min_days_off,
            days=days,
            ga=ga,
        )

    def normalized_days(self) -> List[str]:
        if self.days and len(self.days) >= self.period_days:
            return self.days[: self.period_days]
        if self.period_days <= len(DEFAULT_DAYS):
            return DEFAULT_DAYS[: self.period_days]
        return [f"Hari {idx + 1}" for idx in range(self.period_days)]

    def normalized_shifts(self) -> List[str]:
        return self.shifts if self.shifts else DEFAULT_SHIFTS[:]
