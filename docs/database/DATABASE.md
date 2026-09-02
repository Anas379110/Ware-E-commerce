# DATABASE.md — Ware

قاعدة البيانات: **PostgreSQL** (راجع DECISIONS.md — القرار 007). طبقة مساعدة: **Redis** للسلة المؤقتة/الجلسات فقط — لا تُعتبر مصدر البيانات الدائم.

---

## الكيانات (Entities) — مستخرجة من SRS وTRACEABILITY

| الكيان | الوصف |
|---|---|
| `User` | حساب المستخدم (مشترٍ) — المدير يُدار عبر Django Superuser/Staff منفصل |
| `Address` | عناوين شحن مرتبطة بالمستخدم |
| `Category` | تصنيف منتجات، يدعم التداخل (Parent/Child) |
| `Product` | المنتج الأساسي |
| `ProductImage` | صور متعددة لكل منتج |
| `Cart` | سلة مرتبطة بمستخدم أو بجلسة زائر |
| `CartItem` | عنصر داخل السلة |
| `Order` | الطلب النهائي بعد Checkout |
| `OrderItem` | عنصر داخل الطلب (نسخة ثابتة من بيانات المنتج وقت الشراء) |
| `Payment` | سجل عملية الدفع (Stripe/شام كاش) المرتبطة بالطلب |

---

## العلاقات (Relationships)
- `User` 1 — N `Address`
- `User` 1 — 1 `Cart` (سلة نشطة واحدة لكل مستخدم مسجّل؛ الزائر غير المسجَّل تُربط سلته بمعرّف جلسة عبر Redis)
- `Cart` 1 — N `CartItem`
- `CartItem` N — 1 `Product`
- `Category` 1 — N `Category` (تصنيف ذاتي للتداخل: Parent/Child)
- `Category` 1 — N `Product`
- `Product` 1 — N `ProductImage`
- `User` 1 — N `Order`
- `Order` 1 — N `OrderItem`
- `OrderItem` N — 1 `Product`
- `Order` 1 — 1 `Payment` (كل طلب له سجل دفع واحد؛ محاولات دفع فاشلة متعددة تُسجَّل كسجلات Payment منفصلة مرتبطة بنفس الطلب إذا لزم — يُحسم التفصيل عند التنفيذ الفعلي)

---

## Schema (تخطيطي — الحقول الأساسية فقط)

### User
`id (PK)`, `email (unique)`, `password_hash`, `full_name`, `phone`, `is_active`, `date_joined`

### Address
`id (PK)`, `user_id (FK → User)`, `full_name`, `phone`, `city`, `street_details`, `is_default`

### Category
`id (PK)`, `parent_id (FK → Category, nullable)`, `name`, `slug (unique)`, `is_active`

### Product
`id (PK)`, `category_id (FK → Category)`, `name`, `slug (unique)`, `description`, `price (Decimal)`, `stock_quantity (Integer)`, `is_active`, `created_at`, `updated_at`

### ProductImage
`id (PK)`, `product_id (FK → Product)`, `image_url`, `is_primary`, `order`

### Cart
`id (PK)`, `user_id (FK → User, nullable للزائر)`, `created_at`, `updated_at`

### CartItem
`id (PK)`, `cart_id (FK → Cart)`, `product_id (FK → Product)`, `quantity (Integer, Check > 0)`

### Order
`id (PK)`, `user_id (FK → User)`, `address_id (FK → Address)`, `status (pending/confirmed/shipped/delivered/cancelled/failed)`, `total_amount (Decimal)`, `created_at`, `updated_at`

### OrderItem
`id (PK)`, `order_id (FK → Order)`, `product_id (FK → Product)`, `product_name_snapshot`, `unit_price_snapshot (Decimal)`, `quantity (Integer)`

### Payment
`id (PK)`, `order_id (FK → Order)`, `provider (stripe/sham_cash)`, `provider_reference_id`, `status (pending/succeeded/failed)`, `amount (Decimal)`, `raw_webhook_payload (JSONB — للتدقيق فقط)`, `created_at`

---

## القيود (Constraints)
- `email` فريد (Unique) على `User`
- `slug` فريد على `Category` و`Product`
- `quantity > 0` على `CartItem` و`OrderItem` (Check Constraint)
- `price >= 0` و`stock_quantity >= 0` على `Product` (Check Constraint)
- `status` على `Order` و`Payment` محصور بقيم Enum محددة (Check Constraint أو Django Choices)
- Foreign Keys إلزامية بين كل الجداول المرتبطة أعلاه، مع `on_delete` يُحدَّد حسب المنطق (مثال: حذف `Product` لا يحذف `OrderItem` القديمة — استخدام `product_id` كـ Snapshot يحمي من هذا أصلاً)

## الفهارس (Indexes)
- `Product.slug`, `Product.category_id`, `Product.is_active` (فهارس بحث/فلترة أساسية)
- `Order.user_id`, `Order.status` (للوحة الإدارة والاستعلامات المتكررة)
- `Payment.order_id`, `Payment.provider_reference_id` (لمطابقة Webhooks بسرعة)

## استراتيجية Migration
Django Migrations القياسية. لأي تغيير مستقبلي على Schema بعد الإنتاج: اتباع نمط **Expand → Migrate → Contract** (إضافة عمود جديد أولاً، نقل البيانات، ثم حذف القديم لاحقاً) بدل تعديل مباشر خطر — حسب المرجع الأساسي للمشروع.

## Seed Data
بيانات أولية لكل بيئة (Development/Staging): تصنيفات نموذجية، عدد محدود من المنتجات التجريبية، مستخدم Admin افتراضي (بكلمة مرور تُولَّد وتُحفَظ في `.env` محلياً — لا تُرفَع أبداً لـ Git).
