# Test Cases — Register (Given/When/Then)

## API Contract
- `POST /auth/register`
- 201 success, 409 duplicate, 422 validation

---

## TC-01 — AUTH-REG-001 (Valid register)
**Given**
- API is running
- No existing user with email `test1@gmail.com`
- Request body is prepared with valid input

**When**
- Send `POST /auth/register` with:
```json
{
  "email": "test1@gmail.com",
  "password": "Güçlü.Parola1!",
  "confirm_password": "Güçlü.Parola1!"
}
```

**Then**
- Assert status code is `201`
- Assert response body contains `user_id` and it is not empty
- Assert response body `email` equals `test1@gmail.com`
- Assert user is created (registering again with the same email returns `409`)

---

## TC-02 — AUTH-REG-002 (confirm_password mismatch)
**Given**
- API is running
- No existing user with email `test2@gmail.com`
- Request body is prepared where `confirm_password` does NOT match `password`

**When**
- Send `POST /auth/register` with:
```json
{
  "email": "test2@gmail.com",
  "password": "Güçlü.Parola1!",
  "confirm_password": "Güçlü.Parola123!"
}
```

**Then**
- Assert status code is `422`
- Assert response body `error_code` equals `VALIDATION_ERROR`
- Assert response body `details` includes an item with `field = "confirm_password"`
- Assert the `details` item message indicates mismatch
- Assert user is NOT created (a valid registration with the same email succeeds later with `201`)

---

## TC-03 — AUTH-REG-003 (Weak password)
**Given**
- API is running
- No existing user with email `test3@gmail.com`
- Request body is prepared with a weak password

**When**
- Send `POST /auth/register` with:
```json
{
  "email": "test3@gmail.com",
  "password": "123",
  "confirm_password": "123"
}
```

**Then**
- Assert status code is `422`
- Assert response body `error_code` equals `VALIDATION_ERROR`
- Assert response body `details` includes an item with `field = "password"`
- Assert the `details` item message indicates password policy violation/too weak
- Assert user is NOT created (a valid registration with the same email succeeds later with `201`)

---

## TC-04 — AUTH-REG-004 (Invalid email format)
**Given**
- API is running
- No existing user with email `test4gmail.com`
- Request body is prepared with an invalid email format (missing `@`)

**When**
- Send `POST /auth/register` with:
```json
{
  "email": "test4gmail.com",
  "password": "Güçlü.Parola1!",
  "confirm_password": "Güçlü.Parola1!"
}
```

**Then**
- Assert status code is `422`
- Assert response body `error_code` equals `VALIDATION_ERROR`
- Assert response body `details` contains an item with `field = "email"`
- Assert the `details` item message indicates invalid email format
- Assert user is NOT created (a valid registration with the same email succeeds later with `201`)

---

## TC-05 — AUTH-REG-005 (Missing required field: confirm_password)
**Given**
- API is running
- No existing user with email `test5@gmail.com`
- Request body is prepared with `confirm_password` missing

**When**
- Send `POST /auth/register` with:
```json
{
  "email": "test5@gmail.com",
  "password": "Güçlü.Parola1!"
}
```

**Then**
- Assert status code is `422`
- Assert response body `error_code` equals `VALIDATION_ERROR`
- Assert response body `details` contains an item with `field = "confirm_password"`
- Assert the `details` item message indicates required/missing
- Assert user is NOT created (a valid registration with the same email succeeds later with `201`)
