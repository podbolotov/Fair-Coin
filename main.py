import uvicorn
from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from content.result_page import get_result_page_content
from content.main_page import get_main_page_content
from content.quotes import get_random_before_flip_quote, get_random_after_flip_quote
from core.chances import get_chances, write_chances
from core.flip import flip_coin
from core.history import get_history, write_to_history
from core.vars import ServiceVariables
from database.database import Database

database = Database()

app = FastAPI(
    title="Fair Coin",
    description="Брось монетку и получи повышенные шансы выиграть, если проиграл",
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def main_page():
    chances = get_chances(db=database)
    history = get_history(db=database)
    head_chance, tail_chance = chances.HEAD, chances.TAIL
    return get_main_page_content(
        quote=get_random_before_flip_quote(),
        head_chance=head_chance,
        tail_chance=tail_chance,
        history=history
    )


@app.get("/flip", response_class=RedirectResponse)
async def flip():
    chances = get_chances(db=database)

    current_head_chance, current_tail_chance = chances.HEAD, chances.TAIL

    flip_result = flip_coin(head_chance=current_head_chance, tail_chance=current_tail_chance)

    write_to_history(
        db=database,
        result=flip_result.RESULT,
        chances=f'{ServiceVariables.CUSTOM_HEAD_LABEL}: {current_head_chance}%, '
                f'{ServiceVariables.CUSTOM_TAIL_LABEL}: {current_tail_chance}%'
    )

    write_chances(
        db=database,
        head_chance=flip_result.HEAD,
        tail_chance=flip_result.TAIL
    )

    return RedirectResponse(
        url=f'{ServiceVariables.URL}/result?side={flip_result.RESULT}'
            f'&generation_pool={str(flip_result.GENERATION_POOL)}',
        status_code=303
    )


@app.get("/result", response_class=HTMLResponse)
async def result_page(
        side="Вероятно, вы перешли сюда из истории, или изменили URL",
        generation_pool="нет данных"
):
    chances = get_chances(db=database)

    new_head_chance, new_tail_chance = chances.HEAD, chances.TAIL

    history = get_history(db=database)
    return get_result_page_content(
        quote=get_random_after_flip_quote(),
        side=side,
        generation_pool=generation_pool,
        head_chance=new_head_chance,
        tail_chance=new_tail_chance,
        history=history
    )


@app.get("/reset")
async def reset_chances():
    write_chances(
        db=database,
        head_chance=50,
        tail_chance=50
    )
    write_to_history(
        db=database,
        result="<b><сброс шансов></b>",
        chances=f'Установлены шансы:<br> {ServiceVariables.CUSTOM_HEAD_LABEL}: 50%, '
                f'{ServiceVariables.CUSTOM_TAIL_LABEL}: 50%'
    )
    return RedirectResponse(ServiceVariables.URL)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
