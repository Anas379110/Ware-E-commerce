# Ware

منصة تجارة إلكترونية PWA لجميع المنتجات الصناعية والتجارية السورية.

## ما هو المشروع؟
Ware نظام Single-Vendor مكوَّن من Django REST API (خلفية) وNuxt PWA (واجهة)، بدعم دفع Stripe وشام كاش.

## المزايا
تصفح وبحث وفلترة المنتجات، سلة شراء، Checkout كامل، دفع Stripe/شام كاش، حساب مستخدم، لوحة إدارة، تطبيق PWA قابل للتثبيت.

## المعمارية
راجع `ARCHITECTURE.md` والمخططات في `docs/architecture/`.

## المتطلبات
راجع `docs/requirements/SRS.md`.

## التثبيت
### الخادم (Backend)
راجع `backend/README.md`.

### الواجهة (Frontend)
راجع `frontend/README.md` (يُضاف عند اكتمال Gate 7 للواجهة).

## إعداد قاعدة البيانات
راجع `docs/database/DATABASE.md`.

## التشغيل
```bash
# Backend
cd backend && python manage.py runserver

# Frontend
cd frontend && npm run dev
```

## الاختبار
راجع `TESTING.md` (يُنشأ عند بدء Gate 8).

## البناء
```bash
cd frontend && npm run build
```

## النشر
راجع `DEPLOYMENT.md` (يُنشأ عند بدء Gate 9). استراتيجية الاستضافة الأولية موثّقة في `DECISIONS.md` — القرار 010.

## استكشاف الأخطاء
- تأكد من تعبئة `.env` بناءً على `.env.example`
- تأكد من تشغيل PostgreSQL وRedis محلياً أو الاتصال بمزوّد سحابي صحيح
- راجع `STATUS.md` لمعرفة آخر حالة معروفة للمشروع والمشاكل المفتوحة
