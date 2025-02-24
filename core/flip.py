from random import choice, shuffle
from core.vars import ServiceVariables
from models.coins import CoinSidesChances
from models.results import FlipResultWithChances


def flip_coin(head_chance: int, tail_chance: int) -> FlipResultWithChances:
    pass

    coin_head_chance = range(head_chance)
    coin_tail_chance = range(tail_chance)

    coins_bundle = []

    for x in coin_head_chance:
      coins_bundle.append(ServiceVariables.CUSTOM_HEAD_LABEL)

    for x in coin_tail_chance:
      coins_bundle.append(ServiceVariables.CUSTOM_TAIL_LABEL)

    shuffle(coins_bundle)
    random_side = choice(coins_bundle)

    if random_side == ServiceVariables.CUSTOM_HEAD_LABEL:
        if max(coin_tail_chance) + 1 == 90:
            return FlipResultWithChances(HEAD=10, TAIL=90, RESULT=random_side, GENERATION_POOL=coins_bundle)
        else:
            return FlipResultWithChances(
                HEAD=max(coin_head_chance) - 10 + 1,
                TAIL=max(coin_tail_chance) + 10 + 1,
                RESULT=random_side,
                GENERATION_POOL=coins_bundle
            )
    else:
        if max(coin_head_chance) + 1 == 90:
            return FlipResultWithChances(HEAD=90, TAIL=10, RESULT=random_side, GENERATION_POOL=coins_bundle)
        else:
            return FlipResultWithChances(
                HEAD=max(coin_head_chance) + 10 + 1,
                TAIL=max(coin_tail_chance) - 10 + 1,
                RESULT=random_side,
                GENERATION_POOL=coins_bundle
            )
