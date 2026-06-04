# import google.generativeai as genai
# import json

# genai.configure(api_key="AIzaSyClA8tU38FH2_ReM4eHeLGxeNZGlE9i0Rc")

# model = genai.GenerativeModel("gemini-2.5-flash")


# def parse_query_with_ai(text: str):

#     prompt = f"""
#     Extract patient search filters from this query.

#     Query:
#     "{text}"

#     Return ONLY valid JSON.

#     Allowed fields:
#     - patient_name
#     - doctor_name
#     - hospital_name
#     - gender
#     - blood_group
#     - disease
#     - medicine

#     Example:
#     {{
#       "doctor_name": "ravi",
#       "hospital_name": "apollo",
#       "gender": "male"
#     }}
#     """

#     response = model.generate_content(prompt)

#     raw_text = response.text.strip()

#     print("AI RESPONSE:", raw_text)

#     try:
#         raw_text = raw_text.replace("```json", "")
#         raw_text = raw_text.replace("```", "")
#         raw_text = raw_text.strip()

#         return json.loads(raw_text)

#     except Exception as e:
#         print("JSON ERROR:", e)
#         return {}
import google.generativeai as genai
import json
import re #eng only language check
genai.configure(api_key="AIzaSyBItLWwo_3C0eyMfI9WeZkQlSPXKesvycg") #my api key   
model = genai.GenerativeModel("gemini-2.5-flash")
def parse_query_with_ai(text: str):
    if not text:
        return {"error": "Text is required"}
    text = text.strip()
    lower_text = text.lower()
    tanglish_words = [
        "naa", "naan", "nee", "neenga", "unga", "ungal",
    "pesarathu", "pesuren", "kekda", "kekudha",
    "enna", "epdi", "eppadi", "iruka", "irukinga",
    "vanakkam", "sollu", "sollunga", "peyar", "peru",
    "nadanthu", "nadandhu", "pona", "ponathu",
    "vandha", "vandhu", "poga", "poguthu",
    "sapten", "saptiya", "seri", "illa", "ama"
    ]
    if any(word in lower_text.split() for word in tanglish_words):
       return {"error": "Please speak in English only."}
    # Only language check
    if not re.fullmatch(r"[a-zA-Z0-9\s.,+-]+", text):
        return {"error": "Please speak in English only."}
    prompt = f"""
You are a patient medical record search parser.
User query:
"{text}"
Return ONLY valid JSON.
Allowed fields:
- patient_name
- doctor_name
- hospital_name
- gender
- blood_group
- disease
- medicine
- lab_test
- test_result
- dosage
- follow_up_required
- follow_up_date
- contact_number

Rules:
1. If the query is NOT related to patient details, medical records,
hospital, doctor, disease, medicine, blood group, gender,
contact number, visit date, lab test, dosage, or follow-up,
return:
{{"error": "Please ask only patient-related details."}}

2. If the query is patient-related, extract only the available filters.

3. Convert blood group words:
A positive -> A+
A negative -> A-
B positive -> B+
B negative -> B-
AB positive -> AB+
AB negative -> AB-
O positive -> O+
O negative -> O-
Examples:
"patient handled by Dr Kumar"
{{"doctor_name": "kumar"}}

"show female patients in Apollo hospital"
{{"gender": "female", "hospital_name": "apollo"}}

"patients blood group A negative"
{{"blood_group": "A-"}}

"what is my name"
{{"error": "Please ask only patient-related details."}}
"""

    try:
        response = model.generate_content(prompt)#here it sends to gemini ai
        raw_text = response.text.strip()

        raw_text = raw_text.replace("```json", "").replace("```", "").strip() #removes unwanted characters

        return json.loads(raw_text)

    except Exception as e:
        print("AI PARSER ERROR:", e)

        if "429" in str(e) or "quota" in str(e).lower():
            return {"error": "AI search limit reached. Please try again later."} #too much of api req

        return {"error": "Please ask only patient-related details."}


