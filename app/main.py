from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import re
import uuid

app = FastAPI(title="Demo Auth API", version="1.0.0")

# In-memory "DB" (demo only)
_USERS = {}  # email(lower) -> {"user_id": str, "email": str, "password": str}

def is_strong_password(pw: str) -> bool:
    # Basit politika: >=8, en az 1 küçük, 1 büyük, 1 rakam, 1 özel
    if pw is None:
        return False
    if len(pw) < 8:
        return False
    if not re.search(r"[a-z]", pw):
        return False
    if not re.search(r"[A-Z]", pw):
        return False
    if not re.search(r"[0-9]", pw):
        return False
    if not re.search(r"[^A-Za-z0-9]", pw):
        return False
    return True

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    details = []
    for err in exc.errors():
        loc = err.get("loc", [])
        # loc: ("body", "fieldname")
        field = loc[-1] if loc else "unknown"
        msg = err.get("msg", "validation error")
        details.append({"field": str(field), "message": msg})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error_code": "VALIDATION_ERROR", "details": details},
    )

@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest):
    email_norm = payload.email.strip().lower()

    # confirm mismatch
    if payload.password != payload.confirm_password:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_code": "VALIDATION_ERROR",
                "details": [{"field": "confirm_password", "message": "does not match password"}],
            },
        )

    # password policy
    if not is_strong_password(payload.password):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_code": "VALIDATION_ERROR",
                "details": [{"field": "password", "message": "password too weak / policy violation"}],
            },
        )

    # duplicate
    if email_norm in _USERS:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error_code": "EMAIL_ALREADY_EXISTS", "message": "Email is already registered"},
        )

    user_id = str(uuid.uuid4())
    _USERS[email_norm] = {"user_id": user_id, "email": email_norm, "password": payload.password}
    return {"user_id": user_id, "email": email_norm}

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@app.post("/auth/login")
def login(payload: LoginRequest):
    email_norm = payload.email.strip().lower()
    user = _USERS.get(email_norm)
    if not user or user["password"] != payload.password:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error_code": "INVALID_CREDENTIALS", "message": "Email or password is incorrect"},
        )
    # demo token
    token = "demo-token-" + user["user_id"]
    return {"access_token": token, "token_type": "bearer"}
