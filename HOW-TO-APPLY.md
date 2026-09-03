# كيفية تطبيق هذه التحديثات

هذا الأرشيف يحتوي **فقط** الملفات المعدَّلة أو المضافة حديثاً (توسيع النطاق: تقييمات، مفضلة، كوبونات، منتجات ذات صلة، i18n كامل، إعادة تصميم بالأيقونات — راجع DECISIONS.md القرار 011).

## طريقة الدمج
انسخ محتوى هذا الأرشيف فوق مجلد مشروعك الحالي (`ware-project/`)، مع الحفاظ على نفس المسارات — كل ملف هون بيحل مكان نظيره القديم أو يُضاف كملف جديد.

## قائمة الملفات

### وثائق مُحدَّثة (جذر المشروع)
`SCOPE.md`, `DECISIONS.md`, `STATUS.md`, `TASKS.md`, `PROJECT-AUDIT.md`, `TESTING.md`

### Backend — تطبيقات جديدة بالكامل
- `backend/reviews/` (كامل)
- `backend/wishlist/` (كامل)
- `backend/promotions/` (كامل، فيه `tests.py`)

### Backend — ملفات معدَّلة بتطبيقات موجودة
- `backend/config/settings.py` — تسجيل التطبيقات الثلاثة الجديدة
- `backend/config/urls.py` — مسارات API الجديدة
- `backend/catalog/models.py` — حقل `icon` + منتجات ذات صلة + متوسط تقييم
- `backend/catalog/serializers.py` — نفس الإضافات بمستوى الـ API
- `backend/catalog/admin.py` — عرض الأيقونة بلوحة الإدارة
- `backend/orders/models.py` — دعم الكوبون والخصم
- `backend/orders/views.py` — منطق تطبيق الكوبون بـ Checkout
- `backend/orders/serializers.py` — عرض الخصم والكوبون بالطلب

### Frontend — ملفات جديدة بالكامل
- `frontend/locales/ar.json`, `frontend/locales/en.json`
- `frontend/components/CategoryIcon.vue`, `frontend/components/RatingStars.vue`
- `frontend/stores/wishlist.ts`
- `frontend/pages/wishlist.vue`

### Frontend — ملفات معدَّلة (استُبدلت بالكامل)
`frontend/package.json`, `frontend/nuxt.config.ts`, `frontend/app.vue`, `frontend/README.md`,
`frontend/components/ProductCard.vue`,
`frontend/pages/index.vue`, `frontend/pages/checkout.vue`, `frontend/pages/cart.vue`,
`frontend/pages/products/[slug].vue`,
`frontend/pages/account/login.vue`, `frontend/pages/account/register.vue`,
`frontend/pages/orders/index.vue`, `frontend/pages/orders/[id].vue`

## خطوات إلزامية بعد الدمج
1. `cd backend && pip install -r requirements.txt` (لا تبعيات Python جديدة فعلياً بهذه الدفعة، لكن تأكد من التحديث)
2. `python manage.py makemigrations reviews wishlist promotions catalog orders`
3. `python manage.py migrate`
4. `cd frontend && npm install` (لإضافة `@nuxtjs/i18n` و`lucide-vue-next` الجديدتين بـ package.json)
5. `python manage.py test` — تأكد من نجاح `promotions/tests.py` تحديداً (منطق مالي)
