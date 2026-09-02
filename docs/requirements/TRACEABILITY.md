# TRACEABILITY.md — مصفوفة تتبع المتطلبات (Ware)

تربط هذه المصفوفة كل متطلب عمل بمخرجاته التقنية والاختبارية. تُحدَّث بعد كل مرحلة تصميم/تنفيذ (لا تُترك فارغة عند بدء التطوير).

| # | Business Requirement | User Story | Acceptance Criteria (مرجع) | Component/API (يُحدَّد في Gate 5) | Database (يُحدَّد في Gate 5) | Test (يُحدَّد في Gate 8) |
|---|---|---|---|---|---|---|
| 1 | تصفح المنتجات | US-01 | SRS §US-01 | `GET /api/products` | `Product`, `Category` | Unit + Integration |
| 2 | البحث والفلترة | FR-02.3, FR-02.4 | SRS §US-01 | `GET /api/products?search=&category=` | `Product` (indexed fields) | Unit |
| 3 | إضافة للسلة | US-02 | SRS §US-02 | `POST /api/cart/items` | `Cart`, `CartItem` (Redis-backed) | Unit + Integration |
| 4 | الدفع عبر Stripe | US-03 | SRS §US-03 | `POST /api/checkout/stripe`, Webhook `stripe/webhook` | `Order`, `Payment` | Integration + E2E |
| 5 | الدفع عبر شام كاش | US-04 | SRS §US-04 (NEEDS RESEARCH) | يُحدَّد بعد استلام توثيق شام كاش | `Order`, `Payment` | Integration + E2E |
| 6 | إدارة المنتجات | US-05 | SRS §US-05 | Django Admin — `ProductAdmin` | `Product`, `Category`, `ProductImage` | Manual + Admin Smoke Test |
| 7 | إدارة الطلبات | US-06 | SRS §US-06 | Django Admin — `OrderAdmin` | `Order`, `OrderItem` | Manual + Admin Smoke Test |
| 8 | تثبيت PWA | US-07 | SRS §US-07 | `manifest.json`, Service Worker (Nuxt PWA module) | لا يوجد (Frontend فقط) | Lighthouse Audit |
| 9 | تسجيل ودخول المستخدم | FR-04 | (تحتاج User Story منفصلة — تُضاف لاحقاً) | `POST /api/auth/register`, `POST /api/auth/login` | `User` | Unit + Integration + Security Test |

**ملاحظة:** الأعمدة الخاصة بـ Component/API وDatabase أولية (تخطيطية) بناءً على SRS، وستُثبَّت رسمياً في Gate 5 (تصميم قاعدة البيانات وAPI). لا يُسمح بوجود Requirement بلا اختبار مقابل عند الوصول لمرحلة Gate 8.
