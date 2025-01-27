from datetime import date, datetime

from pydantic import BaseModel, PositiveInt

from code.app_typing import Role


class Patient(BaseModel):
    """ Data about single patient """
    id: PositiveInt
    date_of_birth: date
    diagnoses: list[str]
    created_at: datetime


class Login(BaseModel):
    login: str
    password: str


class AllowAuth(BaseModel):
    access_token: str
    expires_at: int


class SuccessfulLogin(BaseModel):
    role: Role
    user_id: int


class ValidateTokenFields(BaseModel):
    role: Role
    user_id: int
    subtoken: str

class Patients(BaseModel):
    patients: list[Patient]
