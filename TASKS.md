# TASKS.md — Ware

تنظيم هرمي: EPIC → Feature → Task → Subtask
لا تتجاوز أي Task مدة يومي عمل تقريباً — يتم تقسيم أي مهمة أكبر عند التنفيذ الفعلي.

---

## EPIC 0 — التأسيس والتخطيط (Gate 1–2)

### Feature: التحقق من الفكرة والتخطيط الأساسي
- [x] تحليل الفكرة والمشكلة والمستخدمين
- [x] اعتماد نموذج المنتج (MLP)
- [x] اعتماد القرارات التقنية الأساسية
- [ ] تحديد الميزانية والجدول الزمني
- [ ] اعتماد نهائي لـ SCOPE.md

---

## EPIC 1 — تحليل المتطلبات (Gate 3) ✅ مكتمل

### Feature: وثيقة المتطلبات (SRS)
- [x] كتابة Functional Requirements كاملة
- [x] كتابة Non-Functional Requirements (أداء، أمان، توفر)
- [x] كتابة User Stories لكل ميزة Must
- [x] كتابة Acceptance Criteria لكل User Story
- [x] كتابة Use Cases للتدفقات الأساسية (تصفح، شراء، دفع)
- [x] إنشاء مصفوفة التتبع (Requirements Traceability)

---

## EPIC 2 — المعمارية والتصميم التقني (Gate 4–5) ✅ مكتمل

### Feature: المعمارية ✅ مكتمل (Gate 4)
- [x] كتابة ARCHITECTURE.md الكامل (مكونات، تواصل، نقاط فشل، توسع)
- [x] رسم مخططات النظام الأساسية (context, container, sequence, data-flow)

### Feature: قاعدة البيانات ✅ مكتمل (Gate 5)
- [x] تحديد الكيانات الأساسية (Entities) بناءً على SRS
- [x] رسم ERD
- [x] تصميم Schema + Constraints + Indexes
- [x] خطة Migrations وSeed Data (موثقة، التنفيذ الفعلي ضمن Gate 7)

### Feature: تصميم API ✅ مكتمل (Gate 5)
- [x] تحديد Endpoints الأساسية (منتجات، سلة، طلبات، مصادقة، دفع)
- [x] توثيق OpenAPI/Swagger
- [x] تصميم استراتيجية المصادقة عبر API (JWT + HttpOnly Refresh Cookie)

### Feature: UI/UX ✅ مكتمل (Gate 5)
- [x] تحديد Design System (ألوان، خطوط، مكونات) بالهوية البصرية لـ Ware
- [x] تحديد الشاشات الأساسية (توثيقي — Wireframes/Mockups الفعلية بأداة خارجية)
- [x] حالات الخطأ/التحميل/الفراغ (Error/Loading/Empty States)
- [x] معايير الإتاحة وRTL موثقة

---

## EPIC 3 — تجهيز أدوات الذكاء الاصطناعي للتطوير (Gate 6) ✅ مكتمل
- [x] إنشاء CLAUDE.md
- [x] إنشاء هيكل `.claude/` (settings.json, settings.local.json, skills/, hooks/, agents/)
- [x] إنشاء AGENTS.md لـ Codex
- [x] إنشاء Hook أمني (فحص Secrets قبل Commit)
- [x] إنشاء `.gitignore` و`.env.example`

---

## EPIC 4 — التطوير (Gate 7)

### Feature: Backend (Django) ✅ مكتمل لنطاق Must
- [x] مشروع Django وإعدادات (settings, urls, JWT, CORS, Redis, Stripe)
- [x] نماذج قاعدة البيانات لكل التطبيقات
- [x] accounts: تسجيل/دخول/تجديد Token/عناوين
- [x] catalog: منتجات/تصنيفات/بحث/فلترة
- [x] cart: سلة مستخدم مسجّل + زائر
- [x] orders: Checkout + عرض الطلبات
- [x] payments: Stripe كامل + بنية شام كاش مؤقتة
- [x] لوحة إدارة (django-unfold) لكل الكيانات الأساسية
- [x] إشعار بريد تأكيد الطلب

### Feature: Frontend (Nuxt) ✅ مكتمل لنطاق Must
- [x] تهيئة المشروع + وحدة PWA (@vite-pwa/nuxt، Manifest بألوان Ware)
- [x] صفحة رئيسية + قائمة منتجات (بحث/فلترة) + تفاصيل منتج
- [x] السلة + Checkout (عنوان + اختيار Stripe/شام كاش)
- [x] تسجيل/دخول + طلباتي + تفاصيل الطلب
- [x] ربط بـ Design System (docs/design/UI-UX.md → assets/css/main.css)

---

## EPIC 5 — الاختبار والأمان (Gate 8) ✅ مكتمل
- [x] كتابة TESTING.md
- [x] Unit/Integration Tests: accounts, catalog, cart, orders (Checkout بكل الحالات)
- [x] اختبارات payments (الأهم): توقيع Webhook غير صالح، تأكيد ناجح، Idempotency
- [x] كتابة SECURITY.md (مراجعة OWASP Top 10 + 3 ثغرات موثّقة)
- [x] إصلاح الثغرة الحرجة #1 (HttpOnly Refresh Token) — بالكود فعلياً + اختبارات محدَّثة
- [ ] توفير أيقونات PWA فعلية (لا يزال Placeholder نصي)
- [ ] تشغيل الاختبارات فعلياً محلياً (لم يحدث بهذه البيئة — لا Django/شبكة متاحين هنا)

---

## EPIC 6 — النشر والتشغيل (Gate 9–10)
- [x] كتابة DEPLOYMENT.md (تنفيذي كامل: Railway, Vercel, Upstash, Stripe Webhook, Rollback, Post-Deploy Checklist)
- [ ] إضافة تخزين سحابي للصور (django-storages + R2/S3) — قبل أي رفع منتجات حقيقي
- [ ] نشر Backend على Railway/Render (يتطلب إجراء منك)
- [ ] نشر Frontend على Vercel (يتطلب إجراء منك)
- [ ] ربط Redis (Upstash) وPostgreSQL المُدارة
- [ ] إعداد Webhook Stripe الفعلي على البيئة المنشورة
- [ ] إتمام Post-Deploy Checklist
- [x] PROJECT-AUDIT.md — تدقيق نهائي شامل مكتمل (12 محوراً)

---

## EPIC 5 — الاختبار والأمان (Gate 8)
سيُفصَّل لاحقاً وفق TESTING.md وSECURITY.md.

---

## EPIC 6 — النشر والتشغيل (Gate 9–10)
سيُفصَّل لاحقاً وفق DEPLOYMENT.md.
