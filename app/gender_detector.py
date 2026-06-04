def detect_gender_from_name(name: str) -> str | None:
    if not name:
        return None

    name = name.lower().strip()

    male_names = {
        "ravi", "rahul", "arun", "kumar", "suresh",
        "vijay", "ajay", "rajesh", "mahesh"
    }

    female_names = {
        "jeni", "jenifer", "priya", "kavya", "divya",
        "anitha", "sneha", "meena", "lakshmi"
    }

    if name in male_names:
        return "male"
    if name in female_names:
        return "female"
    return None