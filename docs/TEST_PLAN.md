# TEST_PLAN — Auth Register/Login (Demo API)

## Amaç
Auth API’nin (Register/Login) temel iş kurallarını doğrulamak ve otomasyon ile regresyon yakalamak.

## Kapsam (In-scope)
- `POST /auth/register`
  - input validation (email format, required fields)
  - password policy
  - confirm_password mismatch
  - duplicate email (409)
- `POST /auth/login`
  - successful login token
  - wrong password / unknown email (401)

## Kapsam Dışı (Out-of-scope)
- Rate limiting / brute force koruması
- Email doğrulama (verification mail)
- Captcha / MFA
- UI testleri (opsiyonel)

## Riskler
- Validasyon davranışının (error_code/details formatı) değişmesi testleri kırabilir.
- Password policy değişirse test dataları güncellenmeli.

## Test Türleri
- API integration tests (pytest + FastAPI TestClient)
- Negatif/edge testler (validation + duplicate + boundary)

## Test Ortamı
- Local: Python venv
- CI: GitHub Actions (ubuntu-latest)

## Entry Criteria
- Repo clone + dependencies installed
- API contract kabul edildi (docs + app kodu)

## Exit Criteria
- Tüm P0 testler geçti
- CI pipeline yeşil
- HTML rapor artifact oluştu

## Deliverables
- `docs/TEST_SCENARIOS_AUTH_REGISTER.md`
- `docs/TEST_CASES_AUTH_REGISTER.md`
- `docs/BUG_REPORTS/BUG-001.md`
- `tests/api/*.py` (8–10+ test)
- `reports/report.html` (CI artifact)
