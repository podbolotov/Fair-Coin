import json
from contextlib import asynccontextmanager
from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

from content.main_page import get_main_page_content
from content.quotes import get_random_before_flip_quote, get_random_after_flip_quote
from content.result_page import get_result_page_content
from core.broadcast_sender import BroadcastSender
from core.chances import get_chances, write_chances
from core.flip import flip_coin
from core.history import get_history, write_to_history
from core.vars import ServiceVariables
from database.database import Database

database = Database()
broadcast_ws = BroadcastSender()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broadcast_ws.generator.asend(None)
    yield


app = FastAPI(
    title="Fair Coin",
    description="Брось монетку и получи повышенные шансы выиграть, если проиграл",
    version="1.1.0",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def main_page():
    chances = get_chances(db=database)
    history = get_history(db=database)
    head_chance, tail_chance = chances.HEAD, chances.TAIL
    last_result = database.get_history()[0][2]
    return get_main_page_content(
        quote=get_random_before_flip_quote(),
        last_result=last_result,
        head_chance=head_chance,
        tail_chance=tail_chance,
        history=history
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await broadcast_ws.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == 'flip':

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

                history = get_history(db=database)

                message = "coin_flip_response"
                payload = {
                    "result": flip_result.RESULT,
                    "new_head_chance": flip_result.HEAD,
                    "new_tail_chance": flip_result.TAIL,
                    "history": history
                }

            elif data == 'reset':
                write_chances(
                    db=database,
                    head_chance=50,
                    tail_chance=50
                )
                write_to_history(
                    db=database,
                    result="<b>Шансы сброшены</b>",
                    chances='<b>Шансы приведены к 50%</b>'
                )
                chances = get_chances(db=database)
                history = get_history(db=database)
                head_chance, tail_chance = chances.HEAD, chances.TAIL
                message = "chances_reset_response"
                payload = {
                    "result": "<b>Шансы сброшены</b>",
                    "new_head_chance": head_chance,
                    "new_tail_chance": tail_chance,
                    "history": history
                }
            else:
                message = "unknown_action"
                payload = None
            await broadcast_ws.push(
                json.dumps({
                    "message": message,
                    "payload": payload
                })
            )
    except WebSocketDisconnect:
        broadcast_ws.remove(websocket)


# @app.get("/push/{message}")
# async def push_to_connected_websockets(message: str):
#     await notifier.push(f"! Push notification: {message} !")

# @app.get("/", response_class=HTMLResponse)
# async def main_page():
#     chances = get_chances(db=database)
#     history = get_history(db=database)
#     head_chance, tail_chance = chances.HEAD, chances.TAIL
#     return get_main_page_content(
#         quote=get_random_before_flip_quote(),
#         head_chance=head_chance,
#         tail_chance=tail_chance,
#         history=history
#     )

# @app.get("/flip", response_class=RedirectResponse)
# async def flip():
#     chances = get_chances(db=database)
#
#     current_head_chance, current_tail_chance = chances.HEAD, chances.TAIL
#
#     flip_result = flip_coin(head_chance=current_head_chance, tail_chance=current_tail_chance)
#
#     write_to_history(
#         db=database,
#         result=flip_result.RESULT,
#         chances=f'{ServiceVariables.CUSTOM_HEAD_LABEL}: {current_head_chance}%, '
#                 f'{ServiceVariables.CUSTOM_TAIL_LABEL}: {current_tail_chance}%'
#     )
#
#     write_chances(
#         db=database,
#         head_chance=flip_result.HEAD,
#         tail_chance=flip_result.TAIL
#     )
#
#     return RedirectResponse(
#         url=f'{ServiceVariables.URL}/result?side={flip_result.RESULT}'
#             f'&generation_pool={str(flip_result.GENERATION_POOL)}',
#         status_code=303
#     )


# @app.get("/result", response_class=HTMLResponse)
# async def result_page(
#         side="Вероятно, вы перешли сюда из истории, или изменили URL",
#         generation_pool="нет данных"
# ):
#     chances = get_chances(db=database)
#
#     new_head_chance, new_tail_chance = chances.HEAD, chances.TAIL
#
#     history = get_history(db=database)
#     return get_result_page_content(
#         quote=get_random_after_flip_quote(),
#         side=side,
#         generation_pool=generation_pool,
#         head_chance=new_head_chance,
#         tail_chance=new_tail_chance,
#         history=history
#     )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
