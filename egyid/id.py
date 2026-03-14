from __future__ import annotations
from datetime import date
from typing import Any, Dict, Optional, Union
from .generator import generate_id
from .governorates import get_governorate_name, get_region
from .utils import sanitize_id
from .validation import is_valid_id_str


class EgyptianNationalId:
    def __init__(self, id_value: Union[str, int]) -> None:
        """Create a new instance from a raw ID value.

        The value is converted to string and sanitized immediately.
        """
        self.id_str: str = sanitize_id(f"{id_value}")

    def __repr__(self) -> str:
        return f"<EgyptianNationalId {self.id_str}>"

    @staticmethod
    def sanitize(id_value: str) -> str:
        return sanitize_id(id_value)

    @classmethod
    def parse(cls, id_value: Union[str, int]) -> "EgyptianNationalId":
        return cls(id_value)

    @classmethod
    def is_valid_id(cls, id_value: Union[str, int]) -> bool:
        try:
            return is_valid_id_str(sanitize_id(f"{id_value}"))
        except Exception:
            return False

    @classmethod
    def check_is_male(cls, id_value: Union[str, int]) -> bool:
        inst = cls(id_value)
        return inst.is_valid() and inst.is_male()

    @classmethod
    def check_is_female(cls, id_value: Union[str, int]) -> bool:
        inst = cls(id_value)
        return inst.is_valid() and inst.is_female()

    @classmethod
    def check_is_adult(cls, id_value: Union[str, int]) -> bool:
        inst = cls(id_value)
        return inst.is_valid() and inst.is_adult()

    # --- Generator ---
    @classmethod
    def generate(cls, options: Optional[Dict[str, Any]] = None) -> str:
        return generate_id(options)

    def is_valid(self) -> bool:
        """Return True if the ID conforms to all validation rules."""
        return is_valid_id_str(self.id_str)

    def get_birth_year(self) -> int:
        century_digit = int(self.id_str[0])
        year = int(self.id_str[1:3])
        century = 1900 if century_digit == 2 else 2000
        return century + year

    def get_birth_month(self) -> int:
        return int(self.id_str[3:5])

    def get_birth_day(self) -> int:
        return int(self.id_str[5:7])

    def get_birth_date(self) -> Optional[date]:
        try:
            return date(
                self.get_birth_year(),
                self.get_birth_month(),
                self.get_birth_day(),
            )
        except ValueError:
            return None

    def get_age(self) -> Optional[int]:
        bd = self.get_birth_date()
        if bd is None:
            return None
        today = date.today()
        age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
        return age

    # convenience property aliases
    @property
    def birth_date(self) -> Optional[date]:
        return self.get_birth_date()

    @property
    def age(self) -> Optional[int]:
        return self.get_age()

    @property
    def gender(self) -> str:
        return self.get_gender()

    @property
    def governorate(self) -> Optional[str]:
        return self.get_governorate_name()

    @property
    def region_name(self) -> str:
        return self.get_region()

    def get_governorate_code(self) -> str:
        return self.id_str[7:9]

    def get_governorate_name(self) -> Optional[str]:
        return get_governorate_name(self.get_governorate_code())

    def get_region(self) -> str:
        return get_region(self.get_governorate_code())

    def get_gender(self) -> str:
        return "female" if int(self.id_str[12]) % 2 == 0 else "male"

    def is_male(self) -> bool:
        return self.get_gender() == "male"

    def is_female(self) -> bool:
        return self.get_gender() == "female"

    def is_adult(self) -> bool:
        age = self.get_age()
        return age is not None and age >= 18

    def is_inside_egypt(self) -> bool:
        return self.get_governorate_code() != "88"

    def to_dict(self) -> Optional[Dict[str, Any]]:
        if not self.is_valid():
            return None
        return {
            "nationalId": self.id_str,
            "birthYear": self.get_birth_year(),
            "birthMonth": self.get_birth_month(),
            "birthDay": self.get_birth_day(),
            "age": self.get_age(),
            "gender": self.get_gender(),
            "governorate": self.get_governorate_name(),
            "region": self.get_region(),
            "insideEgypt": self.is_inside_egypt(),
            "isAdult": self.is_adult(),
        }
