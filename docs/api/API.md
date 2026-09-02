# API.md — Ware

Django REST Framework — API-only Backend يستهلكه Nuxt (راجع DECISIONS.md — القرار 005/006). التوثيق التفصيلي الكامل بصيغة OpenAPI في `openapi.yaml` بنفس المجلد.

## مبادئ التصميم
- **Versioning:** كل المسارات تحت `/api/v1/` من اليوم الأول
- **المصادقة:** JWT (Access + Refresh Token) عبر `djangorestframework-simplejwt` — يُخزَّن Refresh Token في HttpOnly Cookie لتقليل مخاطر XSS
- **Pagination:** Cursor/PageNumber Pagination على كل القوائم (منتجات، طلبات)
- **Validation:** كل Endpoint يستخدم DRF Serializers مع Validation صارم (لا ثقة بأي مدخل من العميل)
- **Rate Limiting:** مفعّل على `login`, `register`, ومسارات الدفع تحديداً (حماية من هجمات القوة الغاشمة)
- **Error Format:** استجابة خطأ موحّدة `{ "error": { "code": "...", "message": "..." } }`

---

## Endpoints الأساسية

### المصادقة (Auth)
| Method | Endpoint | الوصف |
|---|---|---|
| POST | `/api/v1/auth/register` | تسجيل حساب جديد |
| POST | `/api/v1/auth/login` | تسجيل الدخول (يُعيد Access Token) |
| POST | `/api/v1/auth/refresh` | تجديد Access Token |
| POST | `/api/v1/auth/logout` | تسجيل الخروج |
| POST | `/api/v1/auth/password-reset` | طلب إعادة تعيين كلمة المرور |

### الكتالوج (Catalog)
| Method | Endpoint | الوصف |
|---|---|---|
| GET | `/api/v1/products` | قائمة المنتجات (فلترة: `?category=&search=&min_price=&max_price=`) |
| GET | `/api/v1/products/{slug}` | تفاصيل منتج |
| GET | `/api/v1/categories` | قائمة التصنيفات |

### السلة (Cart)
| Method | Endpoint | الوصف |
|---|---|---|
| GET | `/api/v1/cart` | عرض السلة الحالية |
| POST | `/api/v1/cart/items` | إضافة منتج للسلة |
| PATCH | `/api/v1/cart/items/{id}` | تعديل الكمية |
| DELETE | `/api/v1/cart/items/{id}` | حذف عنصر من السلة |

### الطلبات والدفع (Checkout / Orders)
| Method | Endpoint | الوصف |
|---|---|---|
| POST | `/api/v1/checkout` | إنشاء الطلب من السلة الحالية (status=pending) |
| POST | `/api/v1/payments/stripe/create-session` | إنشاء جلسة دفع Stripe للطلب |
| POST | `/api/v1/payments/stripe/webhook` | استقبال تأكيد Stripe (Webhook — لا يستدعيه Nuxt) |
| POST | `/api/v1/payments/sham-cash/initiate` | بدء عملية دفع شام كاش (NEEDS RESEARCH — التفاصيل النهائية معلّقة) |
| POST | `/api/v1/payments/sham-cash/webhook` | استقبال تأكيد شام كاش (NEEDS RESEARCH) |
| GET | `/api/v1/orders` | طلبات المستخدم الحالي |
| GET | `/api/v1/orders/{id}` | تفاصيل طلب واحد |

### الحساب (Account)
| Method | Endpoint | الوصف |
|---|---|---|
| GET | `/api/v1/account/me` | بيانات المستخدم الحالي |
| GET/POST | `/api/v1/account/addresses` | عناوين المستخدم |

---

## ملاحظات أمنية على الـ API (غير قابلة للتفاوض)
- مسارات `webhook` **لا تتطلب** مصادقة JWT عادية، لكنها **تتحقق إلزامياً من توقيع الطلب** الصادر عن Stripe/شام كاش قبل أي معالجة
- لا يُسمح لأي Endpoint غير `webhook` بتغيير حالة `Order` إلى `confirmed` مباشرة
- كل استجابات الأخطاء لا تكشف تفاصيل داخلية (Stack Trace، أسماء جداول قاعدة البيانات)

## الحالة الحالية لتوثيق شام كاش
مسارا `sham-cash/initiate` و`sham-cash/webhook` أعلاه بنية عامة قياسية مؤقتة، وستُعدَّل فور استلام التوثيق الفعلي من جهة التواصل الرسمية (راجع RESEARCH.md) دون التأثير على بقية الـ API.
