# DEPLOYMENT.md — Ware

نشر فعلي بالكامل على Free Tiers (راجع DECISIONS.md — القرار 010). هذا الدليل خطوات تنفيذية حقيقية، لا وصف نظري.

---

## 1. الاستضافة (Hosting)

| المكوّن | الخدمة | الخطة |
|---|---|---|
| Frontend (Nuxt) | Vercel | Free (Hobby) |
| Backend (Django) | Railway أو Render | Free/Hobby Tier |
| PostgreSQL | Railway Postgres أو Neon | Free Tier |
| Redis | Upstash | Free Tier |

---

## 2. نشر الـ Backend (Railway — الخيار الأول)

1. أنشئ مشروعاً جديداً على Railway، اربطه بمستودع Git الخاص بالمشروع (مجلد `backend/` تحديداً كـ Root Directory عند إعداد الخدمة)
2. أضف خدمة **PostgreSQL** من Railway مباشرة (Add Plugin → PostgreSQL) — يوفر `DATABASE_URL` تلقائياً
3. أضف متغيرات البيئة التالية بلوحة Railway (Variables):
   ```
   DEBUG=False
   SECRET_KEY=<قيمة عشوائية قوية — لا تستخدم القيمة الافتراضية بـ settings.py>
   ALLOWED_HOSTS=<نطاق-Railway-الخاص-بك>.up.railway.app
   DATABASE_URL=<يُملأ تلقائياً من خدمة Postgres>
   REDIS_URL=<من Upstash — راجع القسم 4>
   CORS_ALLOWED_ORIGINS=https://<نطاق-Vercel-الخاص-بك>.vercel.app
   FRONTEND_URL=https://<نطاق-Vercel-الخاص-بك>.vercel.app
   REFRESH_COOKIE_SECURE=True
   REFRESH_COOKIE_SAMESITE=None
   JWT_SIGNING_KEY=<قيمة عشوائية أخرى، مختلفة عن SECRET_KEY>
   STRIPE_SECRET_KEY=<من لوحة Stripe>
   STRIPE_WEBHOOK_SECRET=<يُنشأ بالقسم 6 أدناه>
   SHAM_CASH_API_KEY=
   SHAM_CASH_WEBHOOK_SECRET=
   EMAIL_HOST=<مزوّد بريد — راجع القسم 5>
   EMAIL_HOST_USER=
   EMAIL_HOST_PASSWORD=
   DEFAULT_FROM_EMAIL=no-reply@ware.example
   ```
4. أضف أمر البناء والتشغيل (Railway يكتشف Django تلقائياً غالباً، لكن تأكد من):
   - Build: `pip install -r requirements.txt`
   - Start: `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
5. بعد أول نشر ناجح، أنشئ Superuser عبر Railway Shell:
   ```
   python manage.py createsuperuser
   ```

**ملاحظة أمنية حرجة:** `REFRESH_COOKIE_SAMESITE=None` إلزامي هنا لأن Frontend (Vercel) وBackend (Railway) على نطاقين مختلفين (Cross-Site) — و`SameSite=None` يتطلب `Secure=True` إجبارياً (متوفر تلقائياً لأن Railway يوفر HTTPS افتراضياً).

---

## 3. نشر الـ Frontend (Vercel)

1. استورد المستودع على Vercel، حدّد `frontend/` كـ Root Directory
2. Framework Preset: Nuxt.js (يُكتشف تلقائياً)
3. أضف متغير البيئة:
   ```
   NUXT_PUBLIC_API_BASE_URL=https://<نطاق-Railway-الخاص-بك>.up.railway.app/api/v1
   ```
4. Deploy — Vercel يبني وينشر تلقائياً عند كل Push لـ `main`

---

## 4. Redis (Upstash)

1. أنشئ قاعدة Redis جديدة على Upstash (أقرب Region لموقع Railway)
2. انسخ `REDIS_URL` (بصيغة `rediss://...` غالباً — SSL) وضعه بمتغيرات بيئة Railway

---

## 5. البريد الإلكتروني

خيار مجاني بسيط للبداية: **Resend** أو **Brevo (Sendinblue)** بحدود Free Tier كافية لحجم الإطلاق الأول. أضف بيانات SMTP الناتجة إلى `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` بمتغيرات Railway.

---

## 6. إعداد Webhook Stripe الفعلي

1. من لوحة Stripe (Dashboard → Developers → Webhooks) أضف Endpoint جديد:
   ```
   https://<نطاق-Railway-الخاص-بك>.up.railway.app/api/v1/payments/stripe/webhook
   ```
2. اختر الأحداث: `checkout.session.completed`, `checkout.session.expired`
3. انسخ **Signing Secret** الناتج وضعه بـ `STRIPE_WEBHOOK_SECRET` على Railway
4. اختبر الـ Webhook من نفس لوحة Stripe (زر "Send test webhook") وتأكد من استجابة `200 OK`

---

## 7. الدومين (Domain)

- Vercel وRailway يوفران نطاقاً فرعياً مجانياً افتراضياً (`*.vercel.app`, `*.up.railway.app`) — كافٍ للإطلاق التجريبي الأول ضمن ميزانية 300$
- عند توفر دومين مخصص لاحقاً: يُربط من إعدادات كل من Vercel وRailway مباشرة (كلاهما يدعم SSL تلقائي عبر Let's Encrypt)

---

## 8. التخزين (Storage) — صور المنتجات

**تنبيه هام:** Railway/Render لا يوفران تخزيناً دائماً للملفات المرفوعة (Ephemeral Filesystem) — أي صورة تُرفَع عبر `MEDIA_ROOT` محلياً ستُفقَد عند إعادة نشر الخدمة.

**الحل المطلوب قبل رفع أي منتج فعلي:** استخدام تخزين سحابي خارجي (Cloudflare R2 أو AWS S3 Free Tier) عبر `django-storages`. هذا **NEEDS ACTION** غير مكتمل بعد بالكود الحالي — `catalog/models.py` يستخدم `ImageField` الافتراضي المحلي فقط. يُضاف كتحسين قبل أول رفع منتجات حقيقي.

---

## 9. النسخ الاحتياطي (Backup)

- Railway Postgres: يوفر نسخاً احتياطية تلقائية ضمن Free/Hobby Tier بحدود محدودة — تحقق من سياسة الاحتفاظ (Retention) الحالية بلوحة Railway
- **اختبر الاستعادة فعلياً** (Restore Test) بعد أول بيانات حقيقية — لا تعتبر النسخ الاحتياطي ناجحاً لمجرد وجوده

---

## 10. متغيرات البيئة — قائمة كاملة (مرجع سريع)
راجع `.env.example` بجذر المشروع لكل المتغيرات المطلوبة دفعة واحدة.

---

## 11. خطة الرجوع (Rollback)

- **Frontend (Vercel):** كل Deployment سابق محفوظ تلقائياً — Rollback بضغطة واحدة من لوحة Vercel (Deployments → Promote to Production على نسخة سابقة)
- **Backend (Railway):** Railway يحتفظ بسجل Deployments أيضاً — Rollback مشابه من لوحة Railway
- **قاعدة البيانات:** أي Migration خطرة يجب اختبارها على بيئة Staging أولاً (راجع DATABASE.md — استراتيجية Expand→Migrate→Contract) قبل أي تطبيق على الإنتاج

---

## 12. فحص ما بعد النشر (Post-Deploy Checklist)
- [ ] تسجيل حساب جديد فعلياً من الموقع المنشور ونجاح تسجيل الدخول
- [ ] إضافة منتج تجريبي من لوحة الإدارة وظهوره بالمتجر
- [ ] إتمام عملية شراء تجريبية كاملة عبر Stripe (استخدم بطاقة الاختبار `4242 4242 4242 4242`) والتأكد من وصول Webhook وتأكيد الطلب فعلياً
- [ ] التأكد من عدم إمكانية الوصول لـ `/admin/` بدون بيانات دخول صحيحة
- [ ] تشغيل Lighthouse Audit على الموقع المنشور (PWA Score، الأداء، الإتاحة)
- [ ] مراقبة استهلاك حدود Free Tier خلال أول أسبوع (Railway/Vercel/Upstash Dashboards)
