# Frontend — Ware Storefront (Nuxt PWA)

راجع `../docs/design/UI-UX.md` قبل أي تعديل على الألوان أو المكونات، و`../docs/api/API.md` قبل أي تعديل على طريقة استهلاك الـ API.

## التثبيت والتشغيل محلياً

```bash
cd frontend
npm install

cp .env.example .env    # أنشئه إذا لم يوجد، وحدّد NUXT_PUBLIC_API_BASE_URL
npm run dev
```

الموقع: `http://localhost:3000`
يجب أن يكون الـ Backend شغّالاً على `http://localhost:8000` (أو حسب `NUXT_PUBLIC_API_BASE_URL`).

## البنية
| المسار | الوصف |
|---|---|
| `pages/index.vue` | الصفحة الرئيسية — تصفح/بحث/فلترة |
| `pages/products/[slug].vue` | تفاصيل منتج + إضافة للسلة |
| `pages/cart.vue` | السلة |
| `pages/checkout.vue` | إتمام الشراء (عنوان + وسيلة دفع) — محمية بـ `middleware/auth` |
| `pages/account/login.vue` / `register.vue` | المصادقة |
| `pages/orders/index.vue` / `[id].vue` | طلبات المستخدم |
| `stores/auth.ts` | حالة تسجيل الدخول (JWT عبر Cookies) |
| `stores/cart.ts` | حالة السلة |
| `composables/useApi.ts` | استدعاء موحّد لـ Django API مع إرفاق التوكن |
| `assets/css/main.css` | Design Tokens (الألوان الرسمية لـ Ware) |

## ملاحظات مهمة
- **PWA:** مفعّلة عبر `@vite-pwa/nuxt`. أضف أيقونات فعلية في `public/icons/` قبل الإطلاق (راجع `public/icons/README.txt`).
- **الأمان (مُصلَح):** Refresh Token يُدار بالكامل عبر HttpOnly Cookie من الخادم — `stores/auth.ts` لا يقرأه أو يخزّنه أبداً بأي مكان يصل إليه JavaScript. Access Token بذاكرة Pinia فقط (لا Cookie قابل للقراءة)، ويُستعاد بصمت عند إعادة تحميل الصفحة عبر `auth.hydrate()` (راجع SECURITY.md — الثغرة #1، تم إصلاحها).
- **شام كاش:** واجهة `checkout.vue` تستدعي `payments/sham-cash/initiate` الذي لا يزال بنية عامة مؤقتة من جهة الخادم (راجع `backend/README.md`).
