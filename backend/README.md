# Backend — Ware

Django REST API. راجع `../ARCHITECTURE.md` و`../docs/api/API.md` و`../docs/database/DATABASE.md` قبل أي تعديل.

## التثبيت والتشغيل محلياً

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # على Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp ../.env.example .env        # ثم املأ القيم الفعلية داخل backend/.env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

لوحة الإدارة: `http://localhost:8000/admin/`
API: `http://localhost:8000/api/v1/...`

## ملاحظات مهمة
- **شام كاش:** `payments/views.py` يحتوي بنية عامة مؤقتة (`ShamCashInitiateView`, `ShamCashWebhookView`) بانتظار توثيق API الرسمي — راجع تعليقات `TODO(NEEDS RESEARCH)` داخل الملف.
- **الأمان:** لا يُسمح بتفعيل مسار `sham-cash/webhook` بإنتاج فعلي قبل تطبيق تحقق توقيع حقيقي.
- **الاختبارات:** لم تُكتب بعد (Gate 8 القادمة) — راجع `TESTING.md` عند إنشائه.

## بنية التطبيقات
| التطبيق | المسؤولية |
|---|---|
| `accounts` | المستخدمون، المصادقة (JWT)، العناوين |
| `catalog` | المنتجات، التصنيفات، الصور |
| `cart` | السلة (مستخدم مسجّل أو زائر عبر الجلسة) |
| `orders` | Checkout، الطلبات، عناصر الطلب |
| `payments` | Stripe (فعّال) + شام كاش (بنية مؤقتة) |
| `notifications` | إشعارات البريد الإلكتروني |
