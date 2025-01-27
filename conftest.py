""" conftest """
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from code.main import app
from code.models import Base
from code.services import get_db, get_cache
from code.settings import settings


# Maybe I should up additional PG for testing purposes only,
# but for now it is same
TEST_DATABASE_URL = str(settings.db.DATABASE_URL)

bind = create_async_engine(url=TEST_DATABASE_URL, future=True, echo=True)
TestingSession = async_sessionmaker(bind=bind)

SQL_SCRIPT = """
INSERT INTO users (id, role, login, password) 
    VALUES (1, 'patient', 'patient_1', 'qwe123rty456');
INSERT INTO users (id, role, login, password) 
    VALUES (2, 'patient', 'patient_2', 'qwe123rty456');
INSERT INTO users (id, role, login, password) 
    VALUES (3, 'doctor', 'doctor_1', 'qwe12r3ty456');
INSERT INTO users (id, role, login, password) 
    VALUES (4, 'doctor', 'doctor_2', 'qwe12r3t4y56');
INSERT INTO users (id, role, login, password) 
    VALUES (5, 'patient', 'patient_3', 'qw1e2r3t4y56');
INSERT INTO patients (id, user_id, date_of_birth, diagnoses, created_at)  
    VALUES(1, 1, '2003-03-14', ARRAY ['cancer','diabetes'], current_timestamp);
INSERT INTO patients (id, user_id, date_of_birth, diagnoses, created_at) 
    VALUES(2, 2, '1994-09-24', ARRAY ['healthy'], current_timestamp);
INSERT INTO patients (id, user_id, date_of_birth, diagnoses, created_at) 
    VALUES(3, 5, '1994-09-24', ARRAY ['diabetes'], current_timestamp);
INSERT INTO doctors (id, user_id, specialization) 
    VALUES(1, 3, 'oncologist');
INSERT INTO doctors (id, user_id, specialization) 
    VALUES(2, 4, 'therapist');
INSERT INTO patient_doctor_connection (patient_id, doctor_id) 
    VALUES (1, 1);
INSERT INTO patient_doctor_connection (patient_id, doctor_id) 
    VALUES (2, 2);
INSERT INTO patient_doctor_connection (patient_id, doctor_id) 
    VALUES (2, 1);
"""


async def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        await db.close()


@pytest_asyncio.fixture(loop_scope="session")
async def run_fake_db():
    async with bind.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        for query in SQL_SCRIPT.split(";"):
            await conn.execute(text(query))
    yield
    async with bind.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await bind.dispose()


# noinspection PyUnresolvedReferences
app.dependency_overrides[get_db] = override_get_db
