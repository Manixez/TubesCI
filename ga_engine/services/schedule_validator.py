from typing import List, Optional

from ..models.input_model import InputModel
from ..models.schedule_model import ShiftProblem


def validate_input_model(model: InputModel) -> List[str]:
    errors: List[str] = []

    if not model.buildings:
        errors.append("Daftar gedung tidak boleh kosong.")
    if not model.guards:
        errors.append("Daftar satpam tidak boleh kosong.")
    if model.guards_per_shift <= 0:
        errors.append("Satpam per shift harus > 0.")
    if model.period_days <= 0:
        errors.append("Jumlah hari harus > 0.")
    if model.min_days_off < 0:
        errors.append("Hari libur minimum tidak boleh negatif.")
    if model.min_days_off > model.period_days:
        errors.append("Hari libur minimum tidak boleh melebihi jumlah hari.")

    return errors


def capacity_warning(problem: ShiftProblem) -> Optional[str]:
    total_required = (
        len(problem.days)
        * len(problem.shifts)
        * len(problem.buildings)
        * problem.guards_per_shift
    )
    max_per_guard = len(problem.days) - problem.min_days_off
    max_capacity = max_per_guard * len(problem.guards)

    if max_capacity < total_required:
        return (
            "Jumlah satpam tidak mencukupi untuk memenuhi seluruh shift secara adil. "
            "Tambah satpam atau kurangi gedung/shift/hari libur."
        )

    return None
