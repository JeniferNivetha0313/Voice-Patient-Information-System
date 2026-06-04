from fastapi import FastAPI
from sqlalchemy import text
from database import engine

app = FastAPI()

@app.get("/patient/{name}")
def get_patient(name: str):
    query = text("""
        SELECT p.name, p.hospital_name, m.disease, m.medicine
        FROM patient p
        JOIN medical_record m ON p.patient_id = m.patient_id
        WHERE p.name = :name
        LIMIT 10
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"name": name}).fetchall()

    if not result:
        return {"error": "Patient not found"}

    return result