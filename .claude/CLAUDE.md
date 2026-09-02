# CLAUDE.md — Ware

هذا الملف هو الذاكرة الدائمة لمشروع Ware. اقرأ الوثائق المرجعية أدناه قبل أي عمل — لا تعتمد على الذاكرة السابقة فقط.

## Project Overview
Ware: منصة تجارة إلكترونية PWA (Django REST API + Nuxt) لبيع منتجات صناعية وتجارية سورية. Single-Vendor. راجع `PROJECT.md` للتفاصيل الكاملة.

## Current Phase
راجع `STATUS.md` دائماً أولاً — يحتوي المرحلة الحالية والمهام القادمة والمحجوبة.

## Architecture
Layered Modular Monolith على الخادم (Django Apps منفصلة منطقياً: catalog, cart, orders, payments, accounts, notifications) + Client-Server API-based مع Nuxt. راجع `ARCHITECTURE.md` قبل أي تغيير معماري.

## Tech Stack
- Backend: Django + Django REST Framework
- Frontend: Vue.js + Nuxt (PWA)
- Database: PostgreSQL + Redis
- Payments: Stripe + شام كاش
- Admin: Django Admin (django-unfold)
- Hosting: Free Tiers (Vercel / Railway أو Render / Upstash)

## Database
راجع `docs/database/DATABASE.md` و`docs/database/ERD.mmd` قبل أي تغيير على قاعدة البيانات. لا تُنفَّذ أي Migration خطرة مباشرة — اتبع نمط Expand → Migrate → Contract.

## API
راجع `docs/api/API.md` و`docs/api/openapi.yaml`. كل مسار تحت `/api/v1/`. مسارات `webhook` تتحقق إلزامياً من التوقيع قبل أي معالجة — لا استثناء.

## Project Structure
```
ware/
├── config/            # إعدادات Django (settings, urls)
├── catalog/           # المنتجات والتصنيفات
├── cart/               # السلة
├── orders/            # الطلبات
├── payments/          # Stripe + شام كاش
├── accounts/          # المستخدمون والمصادقة
├── notifications/     # إشعارات البريد
└── storefront/        # مشروع Nuxt المنفصل (repo/مجلد مستقل حسب القرار النهائي)
```

## Coding Rules
- لا `TODO` مفتوحة، لا `print`/`console.log` في كود يُدمج بالفرع الرئيسي
- كل Endpoint له DRF Serializer بـ Validation صريح — لا ثقة بأي مدخل من العميل
- Type Hints في كود Python الجديد
- لا Design Pattern إلا لحل مشكلة حقيقية فعلية — البساطة أولاً

## Testing Rules
راجع `TESTING.md` (يُنشأ عند بدء Gate 7/8). الحد الأدنى: Unit لكل Serializer/Service منطقي، Integration لكل Endpoint حساس (خصوصاً `checkout` و`payments`).

## Security Rules
- لا Secrets بالكود مطلقاً — استخدم متغيرات البيئة فقط (`.env`، غير مرفوع لـ Git)
- تحقق من توقيع كل Webhook قبل أي تحديث لحالة الطلب
- Rate Limiting على `login`, `register`, ومسارات الدفع
- راجع `SECURITY.md` (يُنشأ عند بدء Gate 7/8) لأي تفصيل إضافي

## Git Rules
Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`. فروع: `main` (إنتاج فقط) ← `develop` ← `feature/*` / `fix/*` / `hotfix/*`.

## Documentation Rules
أي تغيير في المعمارية أو قاعدة البيانات أو الـ API أو قرار تقني مهم يُسجَّل فوراً في `DECISIONS.md` و`STATUS.md`، ويُحدَّث هذا الملف (`CLAUDE.md`) إذا كان التغيير يؤثر على القواعد أعلاه.

## Commands (تُستكمل عند إعداد المشروع فعلياً في Gate 7)
```
# Backend
python manage.py runserver
python manage.py migrate
python manage.py test

# Frontend
npm run dev
npm run build
```

## Forbidden Practices
- تعديل مباشر لـ Production Database
- تأكيد حالة دفع بناءً على استجابة Frontend فقط
- إضافة Microservices/Kafka/Kubernetes أو أي تعقيد غير مبرر بحجم المشروع الحالي
- تجاوز نطاق Must في SCOPE.md دون تحليل أثر موثّق

## Definition of Done
كود مكتوب + اختبارات ناجحة + مراجعة أمنية أساسية + توثيق محدَّث + لا مشاكل حرجة + Commit واضح (راجع البند 52 في المرجع الأساسي).

## قبل أي مهمة، اقرأ:
- `PROJECT.md` قبل أي تخطيط
- `docs/requirements/SRS.md` قبل تنفيذ أي متطلب
- `ARCHITECTURE.md` قبل أي تغيير معماري
- `DECISIONS.md` قبل تغيير أي قرار معتمد
- `docs/database/DATABASE.md` قبل أي تغيير على قاعدة البيانات
