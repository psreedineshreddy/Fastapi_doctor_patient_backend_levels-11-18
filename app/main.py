from fastapi import FastAPI, Depends

from app.database import Base, engine
from app.models import User, Doctor, Patient
from app.routers import auth, doctor, patient
from app.auth.dependencies import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(patient.router)

@app.get("/")
def root(current_user=Depends(get_current_user)):
    return {"message": "Doctor Patient Backend API"}