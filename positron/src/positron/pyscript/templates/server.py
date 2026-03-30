import asyncio
import struct
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.websockets import WebSocket
from flatted_view import decode, encode
from next_resolver import next_resolver
from reflected_ffi import local

app = FastAPI()


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    (
        next,
        resolve,
    ) = next_resolver()

    nmsp = None

    while True:
        buff = await websocket.receive_bytes()

        if len(buff) < 5:
            continue

        # print("socket frame:", "id", struct.unpack("<i", buff[0:4])[0], "op", buff[4])

        # CONNECT
        if buff[4] == 0:

            async def reflect(id, trap, args, kwargs):
                (
                    uid,
                    promise,
                ) = next()
                body = bytes(encode([id, trap, args, kwargs]))
                frame = struct.pack("<i", uid) + bytes([2]) + body
                await websocket.send_bytes(frame)
                return promise

            nmsp = local(reflect=reflect)

        else:
            payload = decode(buff[5:]) if len(buff) > 5 else None

            # WORKER CALLING SERVER -> return [OK, ERROR] response
            if buff[4] == 1:
                data = [None, None]

                try:
                    value = nmsp.reflect(*payload)
                    while asyncio.iscoroutine(value):
                        value = await value
                    data[0] = value

                except Exception as e:
                    data[1] = str(e)

                body = bytes(encode(data))
                await websocket.send_bytes(buff[0:5] + body)

            # SERVER CALLING WORKER -> resolve promise
            elif buff[4] == 2:
                resolve(struct.unpack("<i", buff[0:4])[0], payload)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_coi_headers(request, call_next):
    if request.url.path == "/sw.js" and request.method == "POST":
        return await request.json()

    response = await call_next(request)
    response.headers.update(
        {
            "Cross-Origin-Opener-Policy": "same-origin",
            "Cross-Origin-Embedder-Policy": "require-corp",
            "Cross-Origin-Resource-Policy": "cross-origin",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Expires": "0",
            "Last-Modified": "0",
            "ETag": "0",
        }
    )

    return response


app.mount(
    "/",
    StaticFiles(directory=Path(__file__).parent / "resources", html=True),
    name="positron",
)
