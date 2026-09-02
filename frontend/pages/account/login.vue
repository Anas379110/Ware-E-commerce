<template>
  <div style="max-width: 380px; margin: 0 auto;">
    <h1 style="margin: 0 0 16px;">تسجيل الدخول</h1>

    <form style="display: grid; gap: 10px;" @submit.prevent="submit">
      <input v-model="email" type="email" placeholder="البريد الإلكتروني" required style="padding: 10px; border-radius: 8px; border: 1px solid #ddd;" />
      <input v-model="password" type="password" placeholder="كلمة المرور" required style="padding: 10px; border-radius: 8px; border: 1px solid #ddd;" />
      <p v-if="error" style="color: var(--color-danger); margin: 0;">{{ error }}</p>
      <button type="submit" class="btn btn-primary" :disabled="loading">{{ loading ? "جارٍ الدخول..." : "دخول" }}</button>
    </form>

    <p class="text-muted" style="margin-top: 14px;">
      ليس لديك حساب؟ <NuxtLink to="/account/register">أنشئ حساباً جديداً</NuxtLink>
    </p>
  </div>
</template>

<script setup>
const auth = useAuthStore();
const router = useRouter();

const email = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

async function submit() {
  loading.value = true;
  error.value = "";
  try {
    await auth.login({ email: email.value, password: password.value });
    router.push("/");
  } catch (e) {
    error.value = "بيانات الدخول غير صحيحة.";
  } finally {
    loading.value = false;
  }
}
</script>
