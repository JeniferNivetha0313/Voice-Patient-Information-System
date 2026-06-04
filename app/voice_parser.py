import re
PATIENT_KEYWORDS = {
    "patient", "patients", "hospital", "doctor", "dr",
    "disease", "medicine", "medical", "record", "records",
    "treated", "handled", "blood", "contact", "fever",
    "diabetes", "flu", "hypertension", "dolo", "paracetamol"
}

NON_ENGLISH_WORDS = {
    "vanakkam", "enna", "epdi", "eppadi", "iruka", "irukinga",
    "saptiya", "seri", "nandri", "tamil", "unga", "yen",
    "naan", "nee", "neenga", "ungal", "peyar"
}

def parse_voice_text(text: str):
    if not text:
        return {"error": "Text is required"}

    text = text.lower().strip()

    if not re.fullmatch(r"[a-zA-Z0-9\s.,+-]+", text):
        return {"error": "Only English language is supported"}

    words = [word.strip(".,+-") for word in text.split()]

    if any(word in NON_ENGLISH_WORDS for word in words):
        return {"error": "Only English language is supported"}

    has_patient_related_word = any(
        word in PATIENT_KEYWORDS
        for word in words
    )

    has_contact_number = re.search(r"\b\d{10}\b", text)

    if not has_patient_related_word and not has_contact_number:
        return {"error": "Please ask only patient-related queries"}

    return {"search_text": text}











