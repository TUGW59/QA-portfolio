# QA Portfolio — Auth (Register/Login) API Tests

Bu repo, QA/Test Otomasyonu için **kanıt odaklı** bir portföy şablonudur:
- Dokümantasyon (test plan, senaryo, test case, bug report)
- Otomatik API testleri (pytest)
- HTML test raporu (pytest-html)
- CI (GitHub Actions: push/PR -> test -> rapor artifact)

## İçerik
- `app/` : Demo Auth API (FastAPI)
- `tests/` : API testleri (pytest)
- `docs/` : Test plan, senaryolar, test case’ler, bug report örnekleri
- `.github/workflows/ci.yml` : CI pipeline
- `.github/ISSUE_TEMPLATE/bug_report.yml` : GitHub bug report formu

---

## Kurulum (Windows)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Testleri Çalıştırma
```bash
pytest -q
```

## HTML Rapor
```bash
pytest --html=reports/report.html --self-contained-html
```
Rapor dosyası: `reports/report.html`

## Uygulamayı Çalıştırma (opsiyonel)
Bu projede testler `TestClient` ile ayağa kaldırmadan koşuyor. İstersen API’yi çalıştırabilirsin:
```bash
uvicorn app.main:app --reload
```
Swagger: `http://127.0.0.1:8000/docs`

---

## Notlar
- Bu repo “öğrenme + kanıt” için tasarlandı. İleride kendi web projenin API’lerini ekleyip aynı yapıyı koruyacaksın.
