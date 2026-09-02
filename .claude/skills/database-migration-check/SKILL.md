# Skill: database-migration-check

## Purpose
التأكد من أن أي تغيير على Schema قاعدة البيانات آمن ومتوافق مع `docs/database/DATABASE.md` قبل تنفيذه.

## When to Use
عند إنشاء أي Django Migration جديدة (إضافة/حذف/تعديل حقل أو جدول).

## Inputs
- `docs/database/DATABASE.md`
- `docs/database/ERD.mmd`
- ملف الـ Migration الجديد

## Preconditions
التغيير موثَّق أولاً كسبب/حاجة واضحة (Feature أو إصلاح محدد).

## Steps
1. هل التغيير يطابق ما هو موثَّق بـ DATABASE.md؟ إذا لا — حدّث DATABASE.md أولاً قبل التنفيذ.
2. هل التغيير يحذف عموداً/جدولاً مباشرة على بيئة فيها بيانات فعلية؟ إذا نعم — يجب اتباع Expand → Migrate → Contract بدل الحذف المباشر.
3. هل تمت إضافة الفهارس (Indexes) اللازمة لأي حقل جديد يُستخدم بالفلترة/البحث؟
4. هل Constraints (Check/Unique/Foreign Key) مطبَّقة حسب ما هو موثَّق؟
5. هل تم اختبار الـ Migration على بيانات تجريبية قبل أي بيئة حقيقية؟

## Rules
- لا Migration مباشرة على Production دون اختبار على Staging أولاً.
- كل تغيير مهم يُسجَّل في DECISIONS.md إذا أثّر على قرار معماري سابق.

## Validation
الـ Migration تعمل بدون أخطاء ولا فقدان بيانات، وDATABASE.md محدَّث ليعكس الواقع الجديد.

## Expected Output
Migration جاهزة + DATABASE.md/ERD.mmd محدَّثان عند الحاجة + ملاحظة مختصرة بالتغيير في STATUS.md.
