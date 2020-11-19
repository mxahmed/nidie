from typing import Dict
from datetime import date


GOV_MAP = {
    "01": "Cairo",
    "02": "Alexandria",
    "03": "Port Said",
    "04": "Suez",
    "11": "Damietta",
    "12": "Al Dakhlia",
    "13": "Al Sharkia",
    "14": "Al Qaliobia",
    "15": "Kafr Alsheekh",
    "16": "Al Gharbia",
    "17": "Al Monuefia",
    "18": "Al Bohira",
    "19": "Al Ismaellia",
    "21": "Al Giza",
    "22": "Beni Suief",
    "23": "Al Fayoum",
    "24": "Al minia",
    "25": "Assyout",
    "26": "Suhag",
    "27": "Quena",
    "28": "Aswan",
    "29": "Luxor",
    "31": "AlBahr AlAhmar",
    "32": "AlWadi AlJadid",
    "33": "Matrouh",
    "34": "North Sinai",
    "35": "South Sinai",
    "88": "Outside Egypt",
}

GENDER_MAP = {0: "female", 1: "male"}
CENTURY_MAP = {
    "2": {"name": "1900 ~ 1999", "offset": 1900},
    "3": {"name": "2000 ~ 2099", "offset": 2000}
}

def data_from_nid(nid: str) -> Dict:
    return {
        "century_code": nid[0],
        "year": nid[1:3],
        "month": nid[3:5],
        "day": nid[5:7],
        "governerate_code": nid[7:9],
        "identity": nid[9:13],
        "check_digit": nid[13]
    }

def birthdate_from_nid(info: Dict) -> date:
    century_code = info.get("century_code")
    offset = CENTURY_MAP.get(century_code).get("offset") 
    year = int(info.get("year")) + offset
    month = int(info.get("month"))
    day = int(info.get("day"))

    try:
        return date(year, month, day)
    except ValueError:
        return None
