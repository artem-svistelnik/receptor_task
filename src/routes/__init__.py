from routes.auth_routes import auth_router


def include_routes(app):
    app.include_router(auth_router)
