
from sqlalchemy import Column, BigInteger, String, Integer, Date, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Patient(Base):
    __tablename__ = "patient"

    patient_id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    contact_number = Column(String(15))
    hospital_name = Column(String(150))
    gender = Column(String(10))
    blood_group = Column(String(5)) 

class MedicalRecord(Base):
    __tablename__ = "medical_record"

    record_id = Column(BigInteger, primary_key=True)
    patient_id = Column(BigInteger, ForeignKey("patient.patient_id"))
    disease = Column(String(150))
    medicine = Column(String(150))
    doctor_name = Column(String(100))
    visit_date = Column(Date)
    dosage = Column(String(100))
    lab_tests = Column(String(255))
    test_results = Column(String(255))
    follow_up_required = Column(String(20))
    follow_up_date = Column(Date)