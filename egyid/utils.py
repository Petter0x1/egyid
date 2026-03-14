from __future__ import annotations

import re


def sanitize_id(id_value: str) -> str:
    """Return digits-only version of the ID, converting Arabic numerals."""
    trans = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    cleaned = id_value.translate(trans)
    return re.sub(r"[^\d]", "", cleaned)


__all__ = ["sanitize_id"]