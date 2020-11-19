from typing import Dict
from datetime import date, datetime

from pydantic import BaseModel, validator

from .utils import GOV_MAP, GENDER_MAP, CENTURY_MAP, data_from_nid, birthdate_from_nid


class NIDRequest(BaseModel):
    """

    """
    nid: str

    @validator('nid', allow_reuse=True, pre=True)
    def validate_nid_info(cls, value):
        """
        validate the provided nid length and it's extracted information.
        """
        if not value.isdigit():
            raise ValueError("National ID must contain only [0-9] digits.")

        if not len(value) == 14:
            raise ValueError("National ID provided is not 14 digits.")

        data = data_from_nid(value)

        # validate centry code.
        century = data.get("century_code")
        if not century in ["2", "3"]:
            raise ValueError("Invalid century code.")

        # validate birthdate as a valid date value and not a future date.
        birthdate = birthdate_from_nid(data)
        if not birthdate or birthdate > date.today():
            raise ValueError("Invalid Birthdate.")

        # validate governorate code.
        gov = data.get("governerate_code")
        if not gov in GOV_MAP:
            raise ValueError("Invalid governerate code.")

        return value

    @property
    def info(self) -> Dict:
        """
        information extracted from a valid national ID.
        """
        data = data_from_nid(self.nid)
        
        century_code = data.get("century_code")
        gov_code = data.get("governerate_code")
        identity = data.get("identity")

        birthdate = birthdate_from_nid(data)

        data.update({
            "governerate": GOV_MAP.get(gov_code),
            "gender": GENDER_MAP.get(int(identity) % 2),
            "century": CENTURY_MAP.get(century_code).get("name"),
            "birthdate": birthdate.strftime("%d %B %Y")
        })

        return data

class NIDResponse(BaseModel):
    """
    Simple model to describe the scheme of our API response,
    and build the response from a valid request.
    """
    century_code: str
    century: str
    year: str
    month: str
    day: str
    birthdate: str
    governerate_code: str
    governerate: str
    identity: str
    gender: str
    check_digit: str

    @classmethod
    def from_request(cls, request: NIDRequest):
        return cls(**request.info)
