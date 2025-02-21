from pydantic import BaseModel

class CoinSidesChances(BaseModel):
    HEAD: int
    TAIL: int