# # from sqlalchemy.orm import Session
# # from sqlalchemy import or_
# # from app.models import Patient, MedicalRecord


# # def get_patient_details(db: Session, filters: dict):

# #     search_text = filters.get("search_text", "").lower()

# #     query = db.query(Patient, MedicalRecord).join(
# #         MedicalRecord,
# #         Patient.patient_id == MedicalRecord.patient_id
# #     )

# #     query = query.filter(
# #         or_(
# #             Patient.name.ilike(f"%{search_text}%"),
# #             Patient.gender.ilike(f"%{search_text}%"),
# #             Patient.blood_group.ilike(f"%{search_text}%"),
# #             Patient.contact_number.ilike(f"%{search_text}%"),
# #             Patient.hospital_name.ilike(f"%{search_text}%"),
# #             MedicalRecord.disease.ilike(f"%{search_text}%"),
# #             MedicalRecord.medicine.ilike(f"%{search_text}%"),
# #             MedicalRecord.doctor_name.ilike(f"%{search_text}%"),
# #         )
# #     )

# #     return query.limit(50).all()


# from sqlalchemy.orm import Session
# from sqlalchemy import or_
# from app.models import Patient, MedicalRecord


# IGNORE_WORDS = {
#     "patient", "patients", "person", "people",
#     "name", "doctor", "dr", "dr.",
#     "who", "what", "where", "when", "why", "how",
#     "has", "have", "having", "had",
#     "show", "give", "get", "find", "search", "tell", "list",
#     "me", "all", "the", "an", "of", "for", "to", "in",
#     "from", "that", "this", "these", "those",
#     "details", "detail", "record", "records", "medical",
#     "handled", "treated", "by", "disease", "medicine",
#     "blood", "group"
# }


# def normalize_blood_group(text: str):
#     text = text.lower()

#     replacements = {
#         "a positive": "A+",
#         "a negative": "A-",
#         "b positive": "B+",
#         "b negative": "B-",
#         "ab positive": "AB+",
#         "ab negative": "AB-",
#         "o positive": "O+",
#         "o negative": "O-",
#         "a+": "A+",
#         "a-": "A-",
#         "b+": "B+",
#         "b-": "B-",
#         "ab+": "AB+",
#         "ab-": "AB-",
#         "o+": "O+",
#         "o-": "O-",
#     }

#     for key, value in replacements.items():
#         if key in text:
#             return value

#     return None


# def get_patient_details(db: Session, filters: dict):

#     search_text = filters.get("search_text", "").lower()

#     query = db.query(Patient, MedicalRecord).join(
#         MedicalRecord,
#         Patient.patient_id == MedicalRecord.patient_id
#     )

#     # ---------------- BLOOD GROUP ----------------
#     blood_group = normalize_blood_group(search_text)

#     if blood_group:
#         query = query.filter(
#             Patient.blood_group == blood_group
#         )

#     # ---------------- DOCTOR ----------------
#     if "dr" in search_text or "doctor" in search_text:

#         words = search_text.replace(".", "").split()

#         for i, word in enumerate(words):

#             if word in ["dr", "doctor"] and i + 1 < len(words):

#                 doctor_name = words[i + 1]

#                 query = query.filter(
#                     MedicalRecord.doctor_name.ilike(
#                         f"%{doctor_name}%"
#                     )
#                 )

#     # ---------------- PATIENT NAME ----------------
#     if "patient" in search_text and "dr" not in search_text:

#         words = search_text.split()

#         if "patient" in words:

#             idx = words.index("patient")

#             if idx + 1 < len(words):

#                 patient_name = words[idx + 1]

#                 query = query.filter(
#                     Patient.name.ilike(
#                         f"%{patient_name}%"
#                     )
#                 )

#     # ---------------- HOSPITAL ----------------
#     if "hospital" in search_text:

#         hospital_words = []

#         words = search_text.split()

#         for i, word in enumerate(words):

#             if word == "hospital" and i > 0:
#                 hospital_words.append(words[i - 1])

#         if hospital_words:

#             query = query.filter(
#                 Patient.hospital_name.ilike(
#                     f"%{' '.join(hospital_words)}%"
#                 )
#             )

#     # ---------------- DISEASE ----------------
#     disease_keywords = [
#         "diabetes",
#         "flu",
#         "fever",
#         "hypertension",
#         "covid",
#         "asthma"
#     ]

#     for disease in disease_keywords:

#         if disease in search_text:

#             query = query.filter(
#                 MedicalRecord.disease.ilike(
#                     f"%{disease}%"
#                 )
#             )

#     # ---------------- MEDICINE ----------------
#     medicine_keywords = [
#         "paracetamol",
#         "metformin",
#         "insulin",
#         "amlodipine"
#     ]

#     for medicine in medicine_keywords:

#         if medicine in search_text:

#             query = query.filter(
#                 MedicalRecord.medicine.ilike(
#                     f"%{medicine}%"
#                 )
#             )

#     return query.limit(50).all()

from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Patient, MedicalRecord
IGNORE_WORDS = {
    "patient", "patients", "who", "what", "where", "when", "why", "how",
    "has", "have", "having", "show", "give", "get", "find", "search",
    "me", "all", "the", "a", "an", "of", "for", "to", "in", "from",
    "details", "record", "records", "medical", "handled", "treated", "by"
} #no more neeed coz of gemini ai
def get_patient_details(db: Session, filters: dict):
    query = db.query(Patient, MedicalRecord).join(
        MedicalRecord,
        Patient.patient_id == MedicalRecord.patient_id
    )

    # ---------------- PATIENT NAME ----------------
    if filters.get("patient_name"):
        query = query.filter(
            Patient.name.ilike(
                f"%{filters['patient_name']}%"
            )
        )

    # ---------------- GENDER ----------------
    # if filters.get("gender"):
    #     query = query.filter(
    #         Patient.gender.ilike(
    #             f"%{filters['gender']}%"
    #         )
    #     )
    if filters.get("gender"):
        query = query.filter(
        Patient.gender == filters["gender"]
    )

    # ---------------- BLOOD GROUP ----------------
    if filters.get("blood_group"):
        query = query.filter(
            Patient.blood_group.ilike(
                f"%{filters['blood_group']}%"
            )
        )

    # ---------------- HOSPITAL ----------------
    if filters.get("hospital_name"):
        query = query.filter(
            Patient.hospital_name.ilike(
                f"%{filters['hospital_name']}%"
            )
        )

    # ---------------- DOCTOR ----------------
    if filters.get("doctor_name"):
        query = query.filter(
            MedicalRecord.doctor_name.ilike(
                f"%{filters['doctor_name']}%"
            )
        )

    # ---------------- DISEASE ----------------
    if filters.get("disease"):
        query = query.filter(
            MedicalRecord.disease.ilike(
                f"%{filters['disease']}%"
            )
        )
    # ---------------- MEDICINE ----------------
    if filters.get("medicine"):
        query = query.filter(
            MedicalRecord.medicine.ilike(
                f"%{filters['medicine']}%"
            )
        )
    # ---------------- CONTACT NUMBER ----------------
    if filters.get("contact_number"):
         query = query.filter(
            Patient.contact_number == filters["contact_number"]
    )
    return query.limit(50).all()
