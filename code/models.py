from __future__ import annotations
from datetime import date, datetime

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from code.app_typing import Diagnosis, Role, Specialization


class Base(AsyncAttrs, DeclarativeBase):
    pass


patient_doctor_connection = Table(
    "patient_doctor_connection",
    Base.metadata,
    Column("patient_id", ForeignKey("patients.id"), primary_key=True),
    Column("doctor_id", ForeignKey("doctors.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[Role] = mapped_column(default="guest", nullable=False)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)


class Doctor(Base):
    __tablename__ = "doctors"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    patients: Mapped[list[Patient]] = relationship(
        secondary=patient_doctor_connection,
        back_populates="doctors",
        cascade = "all, delete"
    )
    specialization: Mapped[Specialization] = mapped_column(nullable=False)


class Patient(Base):
    __tablename__ = "patients"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_of_birth: Mapped[date] = mapped_column(nullable=False)
    # I decide to not add another table, all diagnoses stored as strings
    diagnoses: Mapped[MutableList[Diagnosis]] = mapped_column(
        MutableList.as_mutable(ARRAY(String)), default=[]
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    doctors: Mapped[list[Doctor]] = relationship(
        secondary=patient_doctor_connection,
        back_populates="patients"
    )


# class Diagnosis(Base):
#     __tablename__ = 'diagnoses'
#     ...