"""Insert data

Revision ID: e3a232338fe9
Revises: d3d48ba66fe7
Create Date: 2025-01-26 22:26:03.508894

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3a232338fe9'
down_revision: str | None = 'fe63d142b4a9'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


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


def upgrade() -> None:
    for query in SQL_SCRIPT.split(';'):
        op.execute(query)

def downgrade() -> None:
    op.execute("DELETE FROM patient_doctor_connection CASCADE")
    op.execute("DELETE FROM doctors CASCADE")
    op.execute("DELETE FROM patients CASCADE")
    op.execute("DELETE FROM users CASCADE")
