# Test Scenarios — Register

## API Contract (varsayım)
- Endpoint: `POST /auth/register`
- Body:
```json
{ "email": "...", "password": "...", "confirm_password": "..." }
```
- Success: `201` + `{ "user_id": "...", "email": "..." }`
- Duplicate email: `409` + `{ "error_code": "EMAIL_ALREADY_EXISTS", "message": "..." }`
- Validation error: `422` + `{ "error_code": "VALIDATION_ERROR", "details": [ { "field": "...", "message": "..." } ] }`

## Scenario List (5 örnek)
Format:
`ID | Title | Type | Preconditions | Test Data | Expected Result | Priority`

1. AUTH-REG-001 | Valid email & strong password registers successfully | Positive | No existing user with email=test1@gmail.com | email=test1@gmail.com; password=Güçlü.Parola1!; confirm_password=Güçlü.Parola1! | 201 + user_id not empty + email echoed + user created | P0
2. AUTH-REG-002 | confirm_password mismatch is rejected | Negative | No existing user with email=test2@gmail.com | email=test2@gmail.com; password=Güçlü.Parola1!; confirm_password=Güçlü.Parola123! | 422 + VALIDATION_ERROR + details(field=confirm_password, mismatch) + user NOT created | P0
3. AUTH-REG-003 | Weak password is rejected | Negative | No existing user with email=test3@gmail.com | email=test3@gmail.com; password=123; confirm_password=123 | 422 + VALIDATION_ERROR + details(field=password, weak) + user NOT created | P0
4. AUTH-REG-004 | Invalid email format (missing @) is rejected | Negative | No existing user with email=test4gmail.com | email=test4gmail.com; password=Güçlü.Parola1!; confirm_password=Güçlü.Parola1! | 422 + VALIDATION_ERROR + details(field=email, invalid format) + user NOT created | P0
5. AUTH-REG-005 | Missing required field: confirm_password is rejected | Negative | No existing user with email=test5@gmail.com | email=test5@gmail.com; password=Güçlü.Parola1! (confirm_password missing) | 422 + VALIDATION_ERROR + details(field=confirm_password, required) + user NOT created | P0
