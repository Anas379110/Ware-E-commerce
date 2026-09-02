# SECURITY.md — Ware

## المبادئ الأساسية (غير قابلة للتفاوض)
1. **لا تأكيد دفع إلا عبر Webhook موقَّع ومتحقَّق منه من طرف الخادم.** لا استثناء، ولا اعتماد على استجابة الواجهة الأمامية مطلقاً.
2. **لا خصم مخزون قبل تأكيد الدفع الفعلي.**
3. **لا Secrets بالكود** — كل شيء عبر متغيرات بيئة، `.env` خارج Git دائماً.
4. **كل مدخل من العميل يمر بـ Validation صريح** عبر DRF Serializers — لا ثقة بأي بيانات واردة.

---

## مراجعة أمنية — بمحاكاة مهاجم متمرس (OWASP Top 10)

### 1. Broken Access Control
**السؤال:** هل يمكن لمستخدم الوصول لبيانات مستخدم آخر؟
- `orders`: `OrderListView`/`OrderDetailView` تُصفَّى دائماً بـ `user=self.request.user` — **محمي**
- `accounts`: `AddressListCreateView`/`AddressDetailView` نفس المبدأ — **محمي**
- `payments`: `Payment` غير مكشوف عبر أي Endpoint عام؛ فقط عبر Django Admin (Staff فقط) — **محمي**

### 2. Cryptographic Failures
- كلمات المرور: `AbstractBaseUser.set_password()` (PBKDF2 الافتراضي بـ Django) — **محمي**
- HTTPS: يجب تفعيله إلزامياً على مستوى الاستضافة (Railway/Render/Vercel توفره تلقائياً) — **مسؤولية بيئة النشر، موثّقة بـ DEPLOYMENT.md عند إنشائه**

### 3. Injection (SQL Injection)
- كل الاستعلامات عبر Django ORM (لا Raw SQL بأي مكان بالكود الحالي) — **محمي بنيوياً**

### 4. Insecure Design
- مبدأ "Webhook فقط" للدفع مطبَّق منذ التصميم (ARCHITECTURE.md) وليس إضافة لاحقة — **محمي بالتصميم**
- Idempotency على `confirm_payment()` — يمنع استغلال إعادة إرسال Webhook لخصم مخزون متكرر (مُختبَر في `payments/tests.py`) — **محمي**

### 5. Security Misconfiguration
- `DEBUG=False` افتراضي بالإنتاج (`.env` يتحكم به) — **يعتمد على ضبط `.env` الفعلي وقت النشر — تذكير هام**
- `ALLOWED_HOSTS` يجب تحديدها صراحة بالإنتاج (لا `*`) — **مسؤولية إعداد `.env` عند النشر**

### 6. Vulnerable and Outdated Components
- `requirements.txt` بإصدارات دنيا محددة (`>=`) — يجب تشغيل فحص Dependency (Dependabot/pip-audit) دورياً بعد أول نشر — **NEEDS ACTION عند Gate 9**

### 7. Identification and Authentication Failures
- JWT عبر `djangorestframework-simplejwt`، Access Token عمره 30 دقيقة فقط — **محمي**
- Rate Limiting على `login`/`register` (`throttle_scope = "auth"`, 10/min) يمنع هجمات القوة الغاشمة الأساسية — **محمي جزئياً** (لا يمنع هجوماً موزّعاً من عناوين IP متعددة — يحتاج طبقة WAF/Cloudflare لاحقاً إذا لزم)

### 8. Software and Data Integrity Failures
- `raw_webhook_payload` يُحفَظ للتدقيق فقط، **لا يُستخدم أبداً** بمنطق تحديث الحالة — التحديث الفعلي يعتمد فقط على النتيجة بعد التحقق من التوقيع — **محمي**

### 9. Security Logging and Monitoring Failures
- توقيع Webhook غير صالح يُسجَّل بـ `logger.warning` — **محمي جزئياً**؛ يحتاج ربطاً بأداة تنبيه فعلية (راجع ARCHITECTURE.md — قسم Logging/Monitoring) بعد النشر — **NEEDS ACTION عند Gate 9**

### 10. Server-Side Request Forgery (SSRF)
- لا يوجد بالكود الحالي أي مسار يقبل URL من العميل ويطلبه من الخادم مباشرة — **غير منطبق حالياً**

---

## نقاط ضعف مكتشفة أثناء المراجعة (مُوثَّقة صراحة)

| # | الثغرة المحتملة | طريقة الاستغلال | الأثر | الاحتمالية | الإصلاح | الحالة |
|---|---|---|---|---|---|---|
| 1 | Refresh Token كان يُخزَّن عبر Cookie من طرف العميل (Nuxt) وليس HttpOnly حقيقي | XSS ناجح يقدر يسرق التوكن من JavaScript | متوسط–مرتفع (سرقة جلسة) | منخفضة (يتطلب XSS ناجح أولاً) | نقل تعيين Refresh Token لاستجابة HttpOnly فعلية من Django | **تم الإصلاح** — `accounts/views.py` (`LoginView`/`RefreshView`/`LogoutView`) يضع الـ Cookie بـ `httponly=True` عبر الخادم فقط؛ Refresh Token لم يعد يظهر بجسم أي استجابة JSON إطلاقاً، وFrontend لا يقرأه أو يخزّنه بأي مكان يصل له JavaScript (راجع `frontend/stores/auth.ts`) |
| 2 | `ShamCashWebhookView` حالياً يرفض كل الطلبات (501) لعدم اكتمال التوثيق | لا استغلال ممكن حالياً (المسار معطَّل فعلياً) | لا يوجد حالياً | — | تفعيله لاحقاً مشروط بتطبيق تحقق توقيع فعلي أولاً — موثّق كشرط بالكود نفسه | مفتوحة — بانتظار توثيق شام كاش |
| 3 | لا حد أقصى معلن لعدد محاولات إنشاء الطلبات (`checkout`) لكل مستخدم بالدقيقة | إنشاء طلبات وهمية متكررة (إزعاج تشغيلي أكثر من ثغرة مالية مباشرة) | منخفض | متوسطة | إضافة `throttle_scope` على `CheckoutView` — **تحسين مقترح لـ Gate 9** | مفتوحة — أولوية منخفضة |

## توصية نهائية
**الثغرة الحرجة الوحيدة (رقم 1) تم إصلاحها فعلياً بالكود.** المشروع أصبح **جاهزاً أمنياً للانتقال لمرحلة النشر** من ناحية إدارة الجلسات، مع بقاء البندين 2 و3 كعناصر متابعة غير حرجة.

### تفاصيل تقنية للإصلاح المطبَّق
- `POST /auth/login`: يُعيد `access` فقط بالجسم، ويضع `ware_refresh_token` كـ `HttpOnly` + `Secure` (بالإنتاج) + `SameSite` قابلة للضبط عبر `.env`
- `POST /auth/refresh`: يقرأ التوكن **من الـ Cookie فقط** (`request.COOKIES`)، لا من جسم الطلب — يمنع أي محاولة لانتحال Refresh Token عبر JSON مباشرة
- `POST /auth/logout`: يُبطل (Blacklist) Refresh Token الحالي فعلياً عبر `rest_framework_simplejwt.token_blacklist`، ويحذف الـ Cookie من طرف الخادم
- `ROTATE_REFRESH_TOKENS=True` + `BLACKLIST_AFTER_ROTATION=True`: كل استخدام لـ Refresh Token يُبطل القديم ويصدر جديداً — يقلل نافذة الاستغلال حتى لو تسرّب توكن قديم بطريقة ما
- Frontend: Access Token بذاكرة Pinia فقط (لا Cookie قابل للقراءة من JS)، ويُستعاد بصمت عند إعادة تحميل الصفحة عبر استدعاء `/auth/refresh` (المتصفح يرفق الـ HttpOnly Cookie تلقائياً دون أي كود JavaScript يراه)

---

## قائمة تحقق أمنية قبل النشر (يُرجَع لها بـ Gate 9)
- [x] نقل Refresh Token لـ HttpOnly Cookie حقيقي من الخادم — **تم**
- [ ] `DEBUG=False` و`ALLOWED_HOSTS` مضبوطة صراحة بالإنتاج
- [ ] `SECRET_KEY` عشوائي وقوي (لا القيمة الافتراضية بـ settings.py)
- [ ] HTTPS مفعَّل على مستوى الاستضافة
- [ ] فحص Dependency (`pip-audit` أو ما يعادله)
- [ ] Rate Limiting إضافي على `checkout`
- [ ] تفعيل تنبيه فعلي (Email/Log Alert) عند فشل تحقق توقيع Webhook
