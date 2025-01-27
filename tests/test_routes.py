import pytest
from httpx import AsyncClient, ASGITransport

from code.main import app
import code.messages as messages
from code.schemas import AllowAuth
from tests.mocks import (
    post_login_user_not_found,
    post_login_patient_ok,
    post_login_bad_password,
    post_login_doctor_ok
)


BASE_URL = "http://test"


@pytest.mark.asyncio(loop_scope="session")
async def test_login_user_not_found(run_fake_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        response = await ac.post(
            url="/login",
            json=post_login_user_not_found,
        )
        assert response.status_code == 404


@pytest.mark.asyncio(loop_scope="session")
async def test_login_bad_password(run_fake_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        response = await ac.post(
            url="/login",
            json=post_login_bad_password,
        )
        assert response.status_code == 401
        assert response.json().get("detail") == messages.INCORRECT_PASSWORD


@pytest.mark.asyncio(loop_scope="session")
async def test_login_patient_ok(run_fake_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        response = await ac.post(
            url="/login",
            json=post_login_patient_ok,
        )
        assert response.status_code == 200
        assert AllowAuth.model_validate(response.json())


@pytest.mark.asyncio(loop_scope="session")
async def test_login_doctor_ok(run_fake_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        response = await ac.post(
            url="/login",
            json=post_login_doctor_ok,
        )
        assert response.status_code == 200
        assert AllowAuth.model_validate(response.json())


@pytest.mark.asyncio(loop_scope="session")
async def test_get_patients_by_patient(run_fake_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        login_response = await ac.post(
            url="/login",
            json=post_login_patient_ok,
        )
        bearer = login_response.json().get("access_token")
        patients_response = await ac.get(
            url="/patients",
            headers={"Authorization": f"Bearer {bearer}"},
        )
        assert patients_response.status_code == 403


@pytest.mark.asyncio(loop_scope="session")
async def test_get_patients_by_doctor(run_fake_db):
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url=BASE_URL) as ac:
        login_response = await ac.post(
            url="/login",
            json=post_login_doctor_ok,
        )
        bearer = login_response.json().get("access_token")
        patients_response = await ac.get(
            url="/patients",
            headers={"Authorization": f"Bearer {bearer}"},
        )
        assert patients_response.status_code == 200
        # We have 2 patients related to doctor_1
        assert len(patients_response.json()) == 2
