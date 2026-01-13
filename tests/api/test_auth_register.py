import pytest

def test_register_success_201_and_user_id(client):
    r = client.post("/auth/register", json={
        "email": "test1@gmail.com",
        "password": "Güçlü.Parola1!",
        "confirm_password": "Güçlü.Parola1!"
    })
    assert r.status_code == 201
    data = r.json()
    assert "user_id" in data and data["user_id"]
    assert data["email"] == "test1@gmail.com"

def test_register_confirm_mismatch_422(client):
    r = client.post("/auth/register", json={
        "email": "test2@gmail.com",
        "password": "Güçlü.Parola1!",
        "confirm_password": "Güçlü.Parola123!"
    })
    assert r.status_code == 422
    data = r.json()
    assert data["error_code"] == "VALIDATION_ERROR"
    assert any(d.get("field") == "confirm_password" for d in data.get("details", []))

def test_register_weak_password_422(client):
    r = client.post("/auth/register", json={
        "email": "test3@gmail.com",
        "password": "123",
        "confirm_password": "123"
    })
    assert r.status_code == 422
    data = r.json()
    assert data["error_code"] == "VALIDATION_ERROR"
    assert any(d.get("field") == "password" for d in data.get("details", []))

def test_register_invalid_email_422(client):
    r = client.post("/auth/register", json={
        "email": "test4gmail.com",  # missing @
        "password": "Güçlü.Parola1!",
        "confirm_password": "Güçlü.Parola1!"
    })
    assert r.status_code == 422
    data = r.json()
    assert data["error_code"] == "VALIDATION_ERROR"
    assert any(d.get("field") == "email" for d in data.get("details", []))

def test_register_missing_confirm_password_422(client):
    r = client.post("/auth/register", json={
        "email": "test5@gmail.com",
        "password": "Güçlü.Parola1!"
    })
    assert r.status_code == 422
    data = r.json()
    assert data["error_code"] == "VALIDATION_ERROR"
    # Pydantic error location should be confirm_password
    assert any(d.get("field") == "confirm_password" for d in data.get("details", []))

def test_register_duplicate_email_409(client):
    first = client.post("/auth/register", json={
        "email": "dup_test@gmail.com",
        "password": "Güçlü.Parola1!",
        "confirm_password": "Güçlü.Parola1!"
    })
    assert first.status_code == 201

    second = client.post("/auth/register", json={
        "email": "dup_test@gmail.com",
        "password": "Güçlü.Parola1!",
        "confirm_password": "Güçlü.Parola1!"
    })
    assert second.status_code == 409
    data = second.json()
    assert data["error_code"] == "EMAIL_ALREADY_EXISTS"

def test_register_email_is_trimmed_and_normalized(client):
    r = client.post("/auth/register", json={
        "email": "  Test6@Gmail.com  ",
        "password": "Güçlü.Parola1!",
        "confirm_password": "Güçlü.Parola1!"
    })
    assert r.status_code == 201
    assert r.json()["email"] == "test6@gmail.com"

def test_register_long_email_rejected_or_accepted_consistently(client):
    # This is a simple boundary-ish test: extremely long local part
    long_email = ("a" * 120) + "@gmail.com"
    r = client.post("/auth/register", json={
        "email": long_email,
        "password": "Güçlü.Parola1!",
        "confirm_password": "Güçlü.Parola1!"
    })
    # EmailStr may accept long values; either behavior is ok as long as not 500
    assert r.status_code in (201, 422)

def test_register_missing_email_422(client):
    r = client.post("/auth/register", json={
        "password": "Güçlü.Parola1!",
        "confirm_password": "Güçlü.Parola1!"
    })
    assert r.status_code == 422
    data = r.json()
    assert data["error_code"] == "VALIDATION_ERROR"
    assert any(d.get("field") == "email" for d in data.get("details", []))

def test_register_missing_body_422(client):
    r = client.post("/auth/register", json={})
    assert r.status_code == 422
    data = r.json()
    assert data["error_code"] == "VALIDATION_ERROR"
