/**
 * Composable موحّد لاستدعاء Django API.
 * التوكن يُقرأ من useAuthStore (ذاكرة فقط) — لا Cookie يصل إليه JavaScript
 * إطلاقاً بعد إصلاح SECURITY.md (الثغرة #1). credentials: "include" ضروري
 * لإرفاق HttpOnly Refresh Cookie تلقائياً بمسار /auth/refresh دون أي وصول
 * برمجي مباشر لقيمته.
 */
export function useApi() {
  const config = useRuntimeConfig();

  async function request(path, options = {}) {
    // استيراد ديناميكي لتفادي حلقة استيراد بين useApi وuseAuthStore
    const { useAuthStore } = await import("~/stores/auth");
    const auth = useAuthStore();

    const headers = {
      ...(options.headers || {}),
      ...(auth.accessToken ? { Authorization: `Bearer ${auth.accessToken}` } : {}),
    };

    return await $fetch(path, {
      baseURL: config.public.apiBase,
      headers,
      credentials: "include",
      ...options,
    });
  }

  return { request };
}
