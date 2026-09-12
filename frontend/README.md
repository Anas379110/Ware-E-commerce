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
| `pages/index.vue` | الصفحة الرئيسية — شبكة أقسام بأيقونات + تصفح/بحث/فلترة |
| `pages/products/[slug].vue` | تفاصيل منتج + تقييمات + منتجات ذات صلة + مفضلة |
| `pages/cart.vue` | السلة |
| `pages/checkout.vue` | إتمام الشراء (عنوان + كوبون خصم + وسيلة دفع) — محمية بـ `middleware/auth` |
| `pages/wishlist.vue` | قائمة المفضلة — محمية بـ `middleware/auth` |
| `pages/account/login.vue` / `register.vue` | المصادقة |
| `pages/orders/index.vue` / `[id].vue` | طلبات المستخدم (تعرض الخصم والكوبون المُطبَّق) |
| `stores/auth.ts` | حالة تسجيل الدخول (Access Token بالذاكرة، Refresh عبر HttpOnly Cookie) |
| `stores/cart.ts` | حالة السلة |
| `stores/wishlist.ts` | حالة المفضلة |
| `composables/useApi.ts` | استدعاء موحّد لـ Django API مع إرفاق التوكن |
| `assets/css/main.css` | Design Tokens (الألوان الرسمية لـ Ware) |
| `components/CategoryIcon.vue` | أيقونة ديناميكية من lucide حسب اسم مخزَّن بقاعدة البيانات |
| `components/RatingStars.vue` | نجوم تقييم قابلة لإعادة الاستخدام |
| `locales/ar.json` / `en.json` | نصوص الواجهة بالكامل باللغتين — راجع هذه الملفات قبل إضافة أي نص جديد بالواجهة |

## تعدد اللغات (i18n)
مفعَّل عبر `@nuxtjs/i18n`. زر تبديل اللغة بالهيدر (`app.vue`) يبدّل فوراً بلا إعادة تحميل، ويُغيّر اتجاه الصفحة (RTL/LTR) تلقائياً عبر `useHead` على `<html lang>` و`<html dir>`. أي نص جديد يُضاف بالواجهة **يجب** أن يُضاف كمفتاح بـ `locales/ar.json` و`locales/en.json` معاً، لا كنص عربي أو إنجليزي ثابت بالكود مباشرة.

## الأيقونات
`lucide-vue-next` — أيقونات التصنيفات تُقرأ من حقل `Category.icon` بالخادم (اسم أيقونة نصي مثل `wrench`)، ويحوّلها `CategoryIcon.vue` لمكوّن Vue تلقائياً. عند إضافة تصنيف جديد من لوحة الإدارة، استخدم اسم أيقونة صالحاً من [مكتبة lucide](https://lucide.dev/icons) (بصيغة kebab-case، مثال: `shopping-bag`).

## ملاحظات مهمة
- **PWA:** مفعّلة عبر `@vite-pwa/nuxt`. أضف أيقونات فعلية في `public/icons/` قبل الإطلاق (راجع `public/icons/README.txt`).
- **الأمان (مُصلَح):** Refresh Token يُدار بالكامل عبر HttpOnly Cookie من الخادم — `stores/auth.ts` لا يقرأه أو يخزّنه أبداً بأي مكان يصل إليه JavaScript. Access Token بذاكرة Pinia فقط (لا Cookie قابل للقراءة)، ويُستعاد بصمت عند إعادة تحميل الصفحة عبر `auth.hydrate()` (راجع SECURITY.md — الثغرة #1، تم إصلاحها).
- **شام كاش:** واجهة `checkout.vue` تستدعي `payments/sham-cash/initiate` الذي لا يزال بنية عامة مؤقتة من جهة الخادم (راجع `backend/README.md`).
