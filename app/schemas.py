from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class MedicalRecordResponse(BaseModel):
    disease: str
    medicine: str
    doctor_name: str
    visit_date: date

class PatientResponse(BaseModel):
    name: str
    contact_number: str
    hospital_name: str
    records: List[MedicalRecordResponse]
    