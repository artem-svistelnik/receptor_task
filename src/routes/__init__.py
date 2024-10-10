from routes.auth_routes import auth_router
from routes.event_routes import event_router


def include_routes(app):
    app.include_router(auth_router)
    app.include_router(event_router)
