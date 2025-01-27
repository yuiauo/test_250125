from datetime import datetime
from uuid import uuid4

import jwt
import redis.asyncio as redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy.exc

from code.auth import decode_jwt, encode_jwt
from code.database import AsyncSessionLocal
from code.models import Doctor, User, Patient, patient_doctor_connection
from code.schemas import (
    Login, Patient as PatientModel, SuccessfulLogin, AllowAuth, ValidateTokenFields
)
from code.settings import settings


async def get_db():
    """ Session generator """
    async_session = AsyncSessionLocal()
    try:
        yield async_session
    finally:
        await async_session.close()


async def get_cache() -> redis.Redis:
    host = settings.cache.REDIS_HOST
    port = settings.cache.REDIS_PORT
    client = await redis.Redis(
        host=host,
        port=port,
        decode_responses=True
    ).client()
    try:
        yield client
    finally:
        await client.aclose()


async def put_subtoken(user_id: int, subtoken: str, cache: redis.Redis) -> None:
    await cache.set(
        f"user_{str(user_id)}",
        subtoken,
        settings.jwt.ACCESS_TOKEN_LIFETIME,
    )


async def get_subtoken(user_id: int, cache: redis.Redis) -> str | None:
    return await cache.get(f"user_{str(user_id)}")


async def _new_access_token(
        payload: SuccessfulLogin,
        cache: redis.Redis
) -> str:
    subtoken = uuid4().hex
    await put_subtoken(payload.user_id, subtoken, cache)
    payload = {
        "subtoken": subtoken,
        **payload.model_dump(),
    }
    return encode_jwt(payload)


async def token_data(payload: SuccessfulLogin, cache: redis.Redis) -> AllowAuth:
    expires_at = int(settings.jwt.ACCESS_TOKEN_LIFETIME + \
                     datetime.now().timestamp())
    access_token = await _new_access_token(payload, cache)
    return AllowAuth(access_token=access_token, expires_at=expires_at)


async def validate_access_token(
        access_token: str,
        cache: redis.Redis
) -> ValidateTokenFields | None:
    try:
        decoded = decode_jwt(access_token)
        validated = ValidateTokenFields(**decoded)
        if validated.subtoken == await get_subtoken(validated.user_id, cache):
            return validated
        # else token expired
    except jwt.InvalidTokenError:
        return None


async def get_user_by_login(login: str, db: AsyncSession) -> User | None:
    stmt = select(User).where(User.login == login)
    result = await db.execute(stmt)
    try:
        user = result.scalars().one()
    except sqlalchemy.exc.NoResultFound as e:
        # exception_log(e)
        return None
    return user


async def login(authorization: Login, db: AsyncSession) -> SuccessfulLogin | bool:
    if user := await get_user_by_login(authorization.login, db):
        if authorization.password == user.password:
            return SuccessfulLogin(user_id=user.id, role=user.role)
        else:
            return True
    return False


async def patients_all(user_id: int, db: AsyncSession) -> list[PatientModel] | None:
    stmt = select(Patient) \
        .join(patient_doctor_connection) \
        .join(Doctor).where(Doctor.user_id == user_id)
    result = await db.execute(stmt)
    try:
        patients = result.scalars().all()
        return patients
    except sqlalchemy.exc.NoResultFound as e:
        # exception_log(e)
        return None
