from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from routes import fast_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def create_app() -> FastAPI:
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_tortoise(
        app,
        db_url='sqlite://db.sqlite3',
        modules={'models': ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    register_views(app=app)

    @app.exception_handler(StarletteHTTPException)
    async def my_exception_handler(request, exception):
        return PlainTextResponse(str(exception.detail), status_code=exception.status_code)

    return app


def register_views(app: FastAPI):
    app.include_router(fast_router, tags=['General'])


TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3"
    },
    "apps": {
        "models": {
            "models": [
                "models", "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}
