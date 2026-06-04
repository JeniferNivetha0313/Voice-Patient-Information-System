from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.database import SessionLocal
from app.crud import get_patient_details
from app.ai_parser import parse_query_with_ai

from fastapi import UploadFile, File
from pypdf import PdfReader

app = FastAPI(title="Voice Patient Info API")#creating fast api
app.add_middleware(
    CORSMiddleware,#Allow React frontend to access backend APIs
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173" #my ip address
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")#read data
def root():
    return {"status": "API is running"}

@app.post("/upload-report")
async def upload_report(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    pdf = PdfReader(file.file)
    text = ""

    for page in pdf.pages:
        text += page.extract_text() or ""

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not read PDF text")

    parsed = parse_query_with_ai(text)

    return {
        "filename": file.filename,
        "extracted_text": text[:1000],
        "ai_extracted_data": parsed
    }


@app.post("/voice-query")#receiving data from frontend and processing it
def voice_query(payload: dict):#payload is frontend data
    text = payload.get("text") if payload else None
    previous_filter = payload.get("previous_filter", {}) if payload else {}

    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    
    try:
        parsed = parse_query_with_ai(text)
    except Exception as e:
         print("AI PARSER ERROR:", e)
         parsed = {"error": "Please ask only patient-related details"}

    if "error" in parsed:
           raise HTTPException(status_code=400, detail=parsed["error"])

    if not parsed:
      raise HTTPException(
        status_code=400,
        detail="Could not understand patient query"
     )
    final_filter = {
        **previous_filter,
        **parsed
    }

    db = SessionLocal()

    try:
        results = get_patient_details(db, final_filter)
    finally:
        db.close()

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No matching records found"
        )

    response_data = []





    for patient, record in results:


        response_data.append({
            "name": patient.name,
            "gender": patient.gender,
            "blood_group": patient.blood_group,
            "contact_number": patient.contact_number,
            "hospital": patient.hospital_name,
            "ai_recommendation": "Recommendation feature is available, but AI quota limit may apply.",
            "medical_record": {
                "disease": record.disease,
                "medicine": record.medicine,
                "dosage": record.dosage or "Not Available",
                "doctor_name": record.doctor_name,
                "visit_date": str(record.visit_date),
                "lab_tests": record.lab_tests or "Not Available",
                "test_results": record.test_results or "Not Available",
                "follow_up_required":
                        record.follow_up_required
                    if record.follow_up_required is not None
                    else 0,
                "follow_up_date": str(record.follow_up_date) if record.follow_up_date else "No Visit"
            }

            
        })

    return {
        "applied_filter": final_filter,
        "patients": response_data
    }

