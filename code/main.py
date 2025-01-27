from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

import code.messages as messages
from code.schemas import Login, AllowAuth
from code.services import (
    get_db, get_cache, login as login_, token_data,
    validate_access_token, patients_all
)
from code.settings import settings


app = FastAPI(**settings.api)
bearer_token = HTTPBearer()


@app.post("/login", tags=["Login"])
async def login(
        authorization: Login,
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_cache)
) -> AllowAuth:
    if successful_login := await login_(authorization, db):
        if isinstance(successful_login, bool):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=messages.INCORRECT_PASSWORD,
            )
        return await token_data(successful_login, cache)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=messages.NOT_FOUND.format(
            f"User `{authorization.login}`"
        ),
    )


@app.get("/patients", tags=["Patient"])
async def patients(
        bearer: Annotated[HTTPAuthorizationCredentials, Security(bearer_token)],
        db: AsyncSession = Depends(get_db),
        cache: Redis = Depends(get_cache)
):
    """ Returns a list of patients """
    # TODO: Make common response handler to parse/validate token data
    if not bearer.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=messages.BEARER_AUTH_REQUIRED,
        )
    if validated := await validate_access_token(bearer.credentials, cache):
        match validated.role:
            case "doctor":
                return await patients_all(validated.user_id, db)
            case _:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=messages.FORBIDDEN
                )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=messages.BEARER_AUTH_INCORRECT
    )