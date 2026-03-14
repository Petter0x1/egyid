from __future__ import annotations

import calendar
import random
from datetime import datetime
from typing import Any, Dict, Optional

from .governorates import GOVERNORATES
from .validation import compute_check_digit


def generate_id(options: Optional[Dict[str, Any]] = None) -> str:
    opts = options or {}

    year = opts.get("year", random.randint(1950, datetime.now().year))
    month = opts.get("month", random.randint(1, 12))
    max_day = calendar.monthrange(year, month)[1]
    day = opts.get("day", random.randint(1, max_day))

    if "governorate" in opts:
        gov = str(opts["governorate"]).zfill(2)
    else:
        gov = random.choice(list(GOVERNORATES.keys()))

    century_digit = 3 if year >= 2000 else 2
    year_digits = str(year)[-2:]
    month_digits = str(month).zfill(2)
    day_digits = str(day).zfill(2)

    if "gender" in opts:
        is_female = opts["gender"] == "female"
    else:
        is_female = bool(random.getrandbits(1))

    sequence_start = str(random.randint(0, 999)).zfill(3)
    gender_digit = random.randint(0, 4) * 2 if is_female else random.randint(0, 4) * 2 + 1

    id_without_check = (
        f"{century_digit}{year_digits}{month_digits}{day_digits}{gov}{sequence_start}{gender_digit}"
    )

    check_digit = compute_check_digit(id_without_check)
    return id_without_check + str(check_digit)


__all__ = ["generate_id"]
