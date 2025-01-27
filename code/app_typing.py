from typing import Literal


type Role = Literal[
    "doctor",
    "patient",
    # "guest",
    # "admin"
]
# There should be another tables, but let's declare them as enums,
# Much better to allow to add any diagnosis or spec
type Diagnosis = Literal["cancer", "healthy", "diabetes"]
type Specialization = Literal["oncologist", "therapist", "nutritionist"]
