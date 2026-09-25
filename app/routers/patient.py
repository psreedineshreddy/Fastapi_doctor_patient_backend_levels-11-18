from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.patient import PatientCreate, PatientResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/", response_model=PatientResponse)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
       raise HTTPException(status_code=403, detail="Admin access required")

    new_patient = Patient(
        name=patient.name,
        age=patient.age,
        phone=patient.phone
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient

@router.get("/", response_model=list[PatientResponse])
def get_patients(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    patients = db.query(Patient).all()
    return patients

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if current_user["role"] == "doctor":
        current_user_doctor = db.query(Doctor).filter(
            Doctor.email == current_user["email"]
        ).first()

        if not current_user_doctor or patient not in current_user_doctor.patients:
            raise HTTPException(status_code=403, detail="Access denied")

    return patient