# FastAPI Doctor Patient Backend

A backend application built with FastAPI for managing doctors, patients, authentication, and doctor-patient assignments.

## 1. Setup Instructions

### Requirements

- Python 3.9+
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite

### Installation

Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

Install the required packages:

```
pip install fastapi uvicorn sqlalchemy pydantic-settings "python-jose[cryptography]" "passlib[bcrypt]" python-multipart email-validator
```

Start the application:

```
uvicorn app.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

## 2. Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=doctor_patient_backend_secret_2026
```

The `SECRET_KEY` is used for JWT authentication.

The `.env` file is excluded from Git using `.gitignore`.

## 3. How Authentication Works

1. Register a user using `POST /auth/register`.
2. The password is securely hashed before being stored.
3. Login using `POST /auth/login`.
4. The API returns a JWT access token after successful login.
5. Use the token to access protected APIs.
6. The API validates the token and identifies the user's email and role.
7. Role-based access is applied to protected operations.

## 4. API Flow Overview

### Authentication

- Register a user.
- Login and receive a JWT token.
- Use the token for protected APIs.

### Doctors

- Admin can create doctors.
- Authenticated users can view doctors.
- Admin can update doctors.
- Admin can soft-delete doctors.

### Patients

- Admin can create and view patients.
- Doctors can view only patients assigned to them.
- Patient details are validated before being stored.

### Doctor-Patient Assignment

- Admin can assign patients to doctors.
- Doctors can view only their assigned patients.

## Validation

- Doctor email must be valid and unique.
- Patient age must be greater than `0`.
- Patient phone number must contain `10–15` digits.
- Protected APIs require JWT authentication.
- Admin-only operations require the `admin` role.
- Doctors can access only their assigned patient records.

