from __future__ import annotations
import re
from datetime import datetime
from .governorates import get_governorate_info


_MULTIPLIERS = (2, 7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2)


def _is_valid_date(year: int, month: int, day: int) -> bool:
    try:
        datetime(year, month, day)
        return True
    except ValueError:
        return False


def _compute_check_digit(id_without_check: str) -> int:
    total = sum(int(id_without_check[i]) * _MULTIPLIERS[i] for i in range(13))
    remainder = total % 11
    if remainder == 0:
        return 0
    else:
        return (11 - remainder) % 10


def is_valid_id_str(id_str: str) -> bool:
    if not re.fullmatch(r"\d{14}", id_str):
        return False

    if int(id_str[0]) not in (2, 3):
        return False

    year = int(id_str[1:3])
    month = int(id_str[3:5])
    day = int(id_str[5:7])
    century = 1900 if int(id_str[0]) == 2 else 2000

    if not _is_valid_date(century + year, month, day):
        return False

    if century + year > datetime.now().year:
        return False

    if get_governorate_info(id_str[7:9]) is None:
        return False

    return (_compute_check_digit(id_str[:13]) == int(id_str[13]))


def compute_check_digit(id_without_check: str) -> int:
    return _compute_check_digit(id_without_check)


__all__ = ["is_valid_id_str", "compute_check_digit"]
