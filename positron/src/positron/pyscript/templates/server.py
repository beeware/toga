# import asyncio
from pathlib import Path

from fastapi import FastAPI

# from fastapi.websockets import WebSocker
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# from constants import MAIN_WS
# from reflected_ffi import local
# from reflected_ffi.direct import decode, encode
# from reflected_ffi.direct.js import Null, Promise

# from next_resolver import next_resolver

app = FastAPI()


# @app.websocket("/")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()

#     (
#         next,
#         resolve,
#     ) = next_resolver(str)

#     coincident = -1
#     nmsp = None

#     while True:
#         if coincident < 0:
#             coincident = 0
#             try:
#                 data = decode(await websocket.receive_bytes())
#                 if isinstance(data, list) and data[0] == MAIN_WS:
#                     coincident = 1

#                     async def reflect(*args):
#                         (
#                             uid,
#                             promise,
#                         ) = next()
#                         await websocket.send_bytes(bytes(encode([uid, args])))
#                         return promise

#                     nmsp = local(reflect=reflect)

#             except Exception as e:
#                 pass

#         elif coincident > 0:
#             try:
#                 buff = await websocket.receive_bytes()
#                 data = decode(buff)
#                 if isinstance(data[0], str):
#                     resolve(*data)
#                 else:
#                     try:
#                         value = nmsp.reflect(*data[1])
#                         while asyncio.iscoroutine(value):
#                             value = await value

#                         data[1] = value

#                     except Exception as e:
#                         data[1] = Null
#                         data[2] = e

#                     await websocket.send_bytes(bytes(encode(data)))
#             except Exception as e:
#                 # connection closed
#                 break


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_coi_headers(request, call_next):
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
