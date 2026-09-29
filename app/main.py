import logging

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import User, Doctor, Patient
from app.routers import auth, doctor, patient
from app.auth.dependencies import get_current_user

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("Doctor Patient Backend API started")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(doctor.router, prefix="/api/v1")
app.include_router(patient.router, prefix="/api/v1")

@app.get("/")
def root(current_user=Depends(get_current_user)):
    return {"message": "Doctor Patient Backend API"}