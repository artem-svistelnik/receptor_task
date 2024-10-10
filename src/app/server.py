import asyncio


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvloop
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.db_config import mongo_db_conf
from db_utils.init_destination import init_database
from middlewares.security import SecurityMiddleware
from routes import include_routes


def get_application():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvloop.install()
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        root_path=settings.ROOT_PATH,
    )
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.add_middleware(SecurityMiddleware)
    include_routes(_app)

    @_app.on_event("startup")
    async def startup_db_client():
        _app.mongodb_client = AsyncIOMotorClient(mongo_db_conf.MONGO_URL)
        _app.mongodb = _app.mongodb_client[mongo_db_conf.DATABASE_NAME]
        await init_database(_app.mongodb)

    @_app.on_event("shutdown")
    async def shutdown_db_client():
        _app.mongodb_client.close()

    return _app


app = get_application()
