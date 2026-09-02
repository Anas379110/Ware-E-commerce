# AGENTS.md — Ware

ملف التعليمات الأساسي لـ Codex CLI. المصدر المشترك للحقيقة مع Claude Code هو نفسه: وثائق المشروع + الكود + الاختبارات، وليس ذاكرة أي أداة.

## Project Overview
Ware: منصة تجارة إلكترونية PWA (Django REST API + Nuxt) لبيع منتجات صناعية وتجارية سورية. Single-Vendor. راجع `PROJECT.md`.

## Architecture
راجع `ARCHITECTURE.md`. Layered Modular Monolith (Django) + Client-Server API مع Nuxt. لا Microservices بدون حاجة فعلية.

## Tech Stack
Django + DRF · Vue/Nuxt (PWA) · PostgreSQL + Redis · Stripe + شام كاش · Django Admin (django-unfold) · Free-Tier Hosting.

## Directory Structure
```
ware/
├── config/
├── catalog/
├── cart/
├── orders/
├── payments/
├── accounts/
├── notifications/
└── storefront/   # Nuxt
```

## Commands
```
python manage.py runserver
python manage.py migrate
python manage.py test
npm run dev
npm run build
```
(تُستكمل عند التنفيذ الفعلي في Gate 7)

## Database Rules
راجع `docs/database/DATABASE.md` و`docs/database/ERD.mmd`. أي تغيير Schema بعد الإنتاج: Expand → Migrate → Contract فقط. لا تعديل مباشر خطر.

## API Rules
راجع `docs/api/API.md` و`docs/api/openapi.yaml`. كل مسار تحت `/api/v1/`. مسارات Webhook تتحقق من التوقيع إلزامياً قبل أي تحديث لحالة الطلب — لا استثناء تحت أي ظرف.

## Coding Rules
- لا Secrets بالكود
- Validation صريح على كل Endpoint (DRF Serializers)
- لا Design Pattern دون حاجة حقيقية
- Type Hints في Python الجديد

## Testing
Unit لكل منطق أعمال، Integration لكل Endpoint حساس (خصوصاً `checkout`, `payments`). راجع `TESTING.md` عند توفره.

## Security
- لا Secrets بالكود، لا Passwords نصية
- تحقق توقيع Webhook إلزامي
- Rate Limiting على `login`, `register`, `payments/*`
- HTTPS إجباري بالإنتاج

## Git
Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`). `main` للإنتاج فقط، لا Push مباشر إليه.

## Documentation
أي قرار تقني مهم → `DECISIONS.md`. أي تغيير حالة → `STATUS.md`. حدّث `AGENTS.md` و`CLAUDE.md` معاً إذا تغيّرت القواعد أعلاه — لا يُسمح بأن يصبح أحدهما قديماً مقارنة بالآخر.

## Definition of Done
كود + اختبارات ناجحة + مراجعة أمنية أساسية + توثيق محدَّث + Code Review + Commit واضح.

## Forbidden Actions
- تعديل مباشر لـ Production Database
- تأكيد دفع بدون Webhook موقَّع ومتحقَّق منه
- تجاوز SCOPE.md (نطاق Must) دون تحليل أثر موثّق في PROJECT.md/SCOPE.md
- إضافة تعقيد معماري (Microservices/Kafka/إلخ) دون حاجة فعلية موثقة
