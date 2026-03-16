from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()


# @app.websocket("/")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     ...


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
