from database.database import Database
from models.coins import CoinSidesChances


def get_chances(db: Database) -> CoinSidesChances:
    db_result = db.get_chances()
    return CoinSidesChances(HEAD=db_result.HEAD, TAIL=db_result.TAIL)

def write_chances(db: Database, head_chance: int, tail_chance: int) -> CoinSidesChances:

    db.write_chances(
        head_chance=head_chance,
        tail_chance=tail_chance
    )

    db_result = db.get_chances()
    return db_result
