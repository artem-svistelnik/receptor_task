from fastapi import APIRouter
from jwt_auth.auth_handler import create_access_token
from jwt_auth.schemas import TokenSchema

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", response_model=TokenSchema)
async def get_token():
    token = create_access_token()
    return TokenSchema(access_token=token)
