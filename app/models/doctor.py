from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


doctor_patient = Table(
    "doctor_patient",
    Base.metadata,
    Column("doctor_id", Integer, ForeignKey("doctors.id")),
    Column("patient_id", Integer, ForeignKey("patients.id"))
)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    patients = relationship(
        "Patient",
        secondary=doctor_patient,
        back_populates="doctors"
    )