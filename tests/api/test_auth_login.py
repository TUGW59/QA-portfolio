def test_login_success_returns_token(client):
    # register first
    r = client.post("/auth/register", json={
        "email": "login_test@gmail.com",
        "password": "Güçlü.Parola1!",
        "confirm_password": "Güçlü.Parola1!"
    })
    assert r.status_code == 201

    login = client.post("/auth/login", json={
        "email": "login_test@gmail.com",
        "password": "Güçlü.Parola1!"
    })
    assert login.status_code == 200
    data = login.json()
    assert "access_token" in data and data["access_token"]
    assert data.get("token_type") == "bearer"

def test_login_wrong_password_401(client):
    r = client.post("/auth/register", json={
        "email": "login_wrong@gmail.com",
        "password": "Güçlü.Parola1!",
        "confirm_password": "Güçlü.Parola1!"
    })
    assert r.status_code == 201

    login = client.post("/auth/login", json={
        "email": "login_wrong@gmail.com",
        "password": "WrongPass1!"
    })
    assert login.status_code == 401
    data = login.json()
    assert data["error_code"] == "INVALID_CREDENTIALS"
