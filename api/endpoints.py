from fastapi import APIRouter

from .models import NIDRequest, NIDResponse


router = APIRouter()

@router.post("/extract", response_model=NIDResponse)
def validate_and_extract(nid: NIDRequest):
    """
    validate the provided national id string value
    provided in the request and return it's extracted information.
    """
    return NIDResponse.from_request(nid)
