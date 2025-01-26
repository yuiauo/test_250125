from datetime import date, datetime

from pydantic import BaseModel, PositiveInt,


class Patient(BaseModel):
    """ Data about single patient """
    id: PositiveInt
    date_of_birth: date
    diagnoses: list[str]
    created_at: datetime


class Login:
    username: str
    password: str

# class AllowAuth(BaseModel):
#     access_token
#     expires_in: PositiveInt


class Patients(BaseModel):
    patients: list[Patient]
