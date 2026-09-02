<template>
  <div style="max-width: 380px; margin: 0 auto;">
    <h1 style="margin: 0 0 16px;">إنشاء حساب</h1>

    <form style="display: grid; gap: 10px;" @submit.prevent="submit">
      <input v-model="full_name" placeholder="الاسم الكامل" required style="padding: 10px; border-radius: 8px; border: 1px solid #ddd;" />
      <input v-model="email" type="email" placeholder="البريد الإلكتروني" required style="padding: 10px; border-radius: 8px; border: 1px solid #ddd;" />
      <input v-model="phone" placeholder="رقم الهاتف" style="padding: 10px; border-radius: 8px; border: 1px solid #ddd;" />
      <input v-model="password" type="password" placeholder="كلمة المرور" required style="padding: 10px; border-radius: 8px; border: 1px solid #ddd;" />
      <p v-if="error" style="color: var(--color-danger); margin: 0;">{{ error }}</p>
      <button type="submit" class="btn btn-primary" :disabled="loading">{{ loading ? "جارٍ الإنشاء..." : "إنشاء الحساب" }}</button>
    </form>

    <p class="text-muted" style="margin-top: 14px;">
      لديك حساب؟ <NuxtLink to="/account/login">سجّل الدخول</NuxtLink>
    </p>
  </div>
</template>

<script setup>
const auth = useAuthStore();
const router = useRouter();

const full_name = ref("");
const email = ref("");
const phone = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

async function submit() {
  loading.value = true;
  error.value = "";
  try {
    await auth.register({ full_name: full_name.value, email: email.value, phone: phone.value, password: password.value });
    router.push("/");
  } catch (e) {
    error.value = e?.data?.email?.[0] || "تعذّر إنشاء الحساب — تحقق من البيانات.";
  } finally {
    loading.value = false;
  }
}
</script>
