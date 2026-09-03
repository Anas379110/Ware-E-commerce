<template>
  <div style="max-width: 380px; margin: 0 auto;">
    <h1 style="margin: 0 0 16px;">{{ $t("account.login_title") }}</h1>

    <form style="display: grid; gap: 10px;" @submit.prevent="submit">
      <input v-model="email" type="email" :placeholder="$t('account.email')" required style="padding: 10px; border-radius: 8px; border: 1px solid #ddd;" />
      <input v-model="password" type="password" :placeholder="$t('account.password')" required style="padding: 10px; border-radius: 8px; border: 1px solid #ddd;" />
      <p v-if="error" style="color: var(--color-danger); margin: 0;">{{ error }}</p>
      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? $t("account.logging_in") : $t("account.login_button") }}
      </button>
    </form>

    <p class="text-muted" style="margin-top: 14px;">
      {{ $t("account.no_account") }} <NuxtLink to="/account/register">{{ $t("account.create_account") }}</NuxtLink>
    </p>
  </div>
</template>

<script setup>
const auth = useAuthStore();
const router = useRouter();
const { t } = useI18n();

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
    error.value = t("account.login_error");
  } finally {
    loading.value = false;
  }
}
</script>
