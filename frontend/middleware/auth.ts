import { useAuthStore } from "~/stores/auth";

export default defineNuxtRouteMiddleware(async () => {
  const auth = useAuthStore();

  // يحاول استعادة الجلسة بصمت عبر HttpOnly Cookie قبل الحكم بعدم تسجيل الدخول
  if (!auth.isAuthenticated) {
    await auth.hydrate();
  }

  if (!auth.isAuthenticated) {
    return navigateTo("/account/login");
  }
});
