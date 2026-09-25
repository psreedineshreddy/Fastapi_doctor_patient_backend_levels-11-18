from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/", response_model=DoctorResponse)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    existing_doctor = db.query(Doctor).filter(
        Doctor.email == doctor.email
    ).first()

    if existing_doctor:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_doctor = Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
        email=doctor.email
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor

@router.get("/", response_model=list[DoctorResponse])
def get_doctors(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doctors = db.query(Doctor).all()
    return doctors

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return doctor

@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    existing_doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not existing_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    existing_doctor.name = doctor.name
    existing_doctor.specialization = doctor.specialization
    existing_doctor.email = doctor.email

    db.commit()
    db.refresh(existing_doctor)

    return existing_doctor

@router.delete("/{doctor_id}", response_model=DoctorResponse)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    doctor.is_active = False

    db.commit()
    db.refresh(doctor)

    return doctor

@router.post("/{doctor_id}/patients/{patient_id}")
def assign_patient(
    doctor_id: int,
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
       raise HTTPException(status_code=403, detail="Admin access required")
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if patient not in doctor.patients:
        doctor.patients.append(patient)

    db.commit()

    return {"message": "Patient assigned successfully"}

@router.get("/{doctor_id}/patients")
def get_doctor_patients(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if current_user["role"] == "doctor":
        current_user_doctor = db.query(Doctor).filter(
            Doctor.email == current_user["email"]
        ).first()

        if not current_user_doctor or current_user_doctor.id != doctor_id:
            raise HTTPException(status_code=403, detail="Access denied")

    return doctor.patients