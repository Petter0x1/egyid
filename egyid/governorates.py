from __future__ import annotations

from typing import Dict, Optional, TypedDict


class GovernorateInfo(TypedDict):
    name: str
    region: str


GOVERNORATES: Dict[str, GovernorateInfo] = {
    "01": {"name": "Cairo", "region": "Cairo"},
    "02": {"name": "Alexandria", "region": "Alexandria"},
    "03": {"name": "Port Said", "region": "Canal"},
    "04": {"name": "Suez", "region": "Canal"},
    "11": {"name": "Damietta", "region": "Delta"},
    "12": {"name": "Dakahlia", "region": "Delta"},
    "13": {"name": "Ash Sharqia", "region": "Delta"},
    "14": {"name": "Kalyubia", "region": "Delta"},
    "15": {"name": "Kafr El Sheikh", "region": "Delta"},
    "16": {"name": "Gharbia", "region": "Delta"},
    "17": {"name": "Monufia", "region": "Delta"},
    "18": {"name": "Beheira", "region": "Delta"},
    "19": {"name": "Ismailia", "region": "Canal"},
    "21": {"name": "Giza", "region": "Upper Egypt"},
    "22": {"name": "Beni Suef", "region": "Upper Egypt"},
    "23": {"name": "Fayoum", "region": "Upper Egypt"},
    "24": {"name": "Minya", "region": "Upper Egypt"},
    "25": {"name": "Assiut", "region": "Upper Egypt"},
    "26": {"name": "Sohag", "region": "Upper Egypt"},
    "27": {"name": "Qena", "region": "Upper Egypt"},
    "28": {"name": "Aswan", "region": "Upper Egypt"},
    "29": {"name": "Luxor", "region": "Upper Egypt"},
    "31": {"name": "Red Sea", "region": "Frontier"},
    "32": {"name": "New Valley", "region": "Frontier"},
    "33": {"name": "Matrouh", "region": "Frontier"},
    "34": {"name": "North Sinai", "region": "Frontier"},
    "35": {"name": "South Sinai", "region": "Frontier"},
    "88": {"name": "Outside the Republic", "region": "Foreign"},
}


def get_governorate_info(code: str) -> Optional[GovernorateInfo]:
    return GOVERNORATES.get(code)


def get_governorate_name(code: str) -> Optional[str]:
    info = get_governorate_info(code)
    return info["name"] if info else None


def get_region(code: str) -> str:
    info = get_governorate_info(code)
    return info.get("region", "Foreign") if info else "Foreign"


__all__ = ["GovernorateInfo", "GOVERNORATES", "get_governorate_info", "get_governorate_name", "get_region"]