from models.coins import CoinSidesChances

class FlipResultWithChances(CoinSidesChances):
    RESULT: str
    GENERATION_POOL: list