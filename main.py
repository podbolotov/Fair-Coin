import json
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocketDisconnect

from content.main_page import get_main_page_content
from content.quotes import get_random_before_flip_quote
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
                await broadcast_ws.push(
                    json.dumps({
                        "message": message,
                        "payload": payload
                    })
                )

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
                await broadcast_ws.push(
                    json.dumps({
                        "message": message,
                        "payload": payload
                    })
                )

            elif data == 'repeat_last_for_me_only':
                chances = get_chances(db=database)
                history = get_history(db=database)
                last_result = database.get_history()[0][2]
                head_chance, tail_chance = chances.HEAD, chances.TAIL
                message = "repeat_last_for_you_only_response"
                payload = {
                    "result": last_result,
                    "new_head_chance": head_chance,
                    "new_tail_chance": tail_chance,
                    "history": history
                }
                await broadcast_ws.send_to_one_only(
                    websocket=websocket,
                    message=json.dumps({
                        "message": message,
                        "payload": payload
                    })
                )

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
