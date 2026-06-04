import random
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Letmein@123",
    database="PatientDetails"
)

cursor = conn.cursor()

names = ["Jeni", "Arun", "Karthik", "Meena", "Ravi"]
diseases = ["Diabetes", "Hypertension", "Asthma", "Flu"]
medicines = ["Metformin", "Insulin", "Paracetamol", "Amlodipine"]
hospitals = ["Apollo Hospital", "Fortis", "MIOT"]

BATCH_SIZE = 1000

for i in range(500000):
    name = random.choice(names)

    cursor.execute(
        "INSERT INTO patient (name, age, gender, hospital_name) VALUES (%s,%s,%s,%s)",
        (name, random.randint(20,80), "Female", random.choice(hospitals))
    )
    patient_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO medical_record (patient_id, disease, medicine, doctor_name, visit_date) "
        "VALUES (%s,%s,%s,%s,CURDATE())",
        (patient_id, random.choice(diseases), random.choice(medicines), "Dr. Kumar")
    )

    # Commit every 1000 records
    if (i + 1) % BATCH_SIZE == 0:
        conn.commit()
        print(f"Inserted {i + 1} records")

# Final commit
conn.commit()

cursor.close()
conn.close()

print("✅ 5 lakh patient records inserted successfully")