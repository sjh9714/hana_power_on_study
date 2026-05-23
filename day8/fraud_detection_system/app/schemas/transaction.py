from pydantic import BaseModel

class Transaction(BaseModel):

    cc_num: int

    amt: float

    lat: float
    long: float

    merch_lat: float
    merch_long: float

    hour: int