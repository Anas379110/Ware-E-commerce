#!/usr/bin/env bash
# pre-commit-secrets-check.sh
# يمنع أي Commit يحتوي ملفات أو محتوى حساس (Secrets, Keys, Credentials)

set -e

STAGED_FILES=$(git diff --cached --name-only)

# 1) منع ملفات حساسة معروفة
BLOCKED_PATTERNS='(^|/)\.env($|\.)|\.pem$|\.key$|credentials|id_rsa'
if echo "$STAGED_FILES" | grep -E "$BLOCKED_PATTERNS" > /dev/null; then
  echo "❌ تم رفض الـ Commit: يحتوي على ملف محظور (env/pem/key/credentials)."
  echo "$STAGED_FILES" | grep -E "$BLOCKED_PATTERNS"
  exit 1
fi

# 2) فحص محتوى الملفات المرحّلة بحثاً عن أنماط مفاتيح API شائعة
SECRET_PATTERNS='AKIA[0-9A-Z]{16}|sk_live_[0-9a-zA-Z]+|sk_test_[0-9a-zA-Z]+|-----BEGIN (RSA |EC |)PRIVATE KEY-----'

for file in $STAGED_FILES; do
  if [ -f "$file" ]; then
    if grep -EqI "$SECRET_PATTERNS" "$file"; then
      echo "❌ تم رفض الـ Commit: احتمال وجود مفتاح/سر حساس داخل: $file"
      exit 1
    fi
  fi
done

echo "✅ فحص الأسرار قبل الـ Commit: لا مشاكل."
exit 0
