import { defineStore } from "pinia";

/**
 * إدارة المصادقة — بعد إصلاح SECURITY.md (الثغرة #1):
 * - Access Token يُحفَظ فقط بذاكرة المتصفح (Pinia state)، لا بأي Cookie يصل إليه JavaScript.
 * - Refresh Token لا يصل لهذا الملف إطلاقاً — يُدار بالكامل عبر HttpOnly Cookie من الخادم
 *   (راجع backend/accounts/views.py — _set_refresh_cookie).
 * - عند تحميل الصفحة من جديد، نستدعي hydrate() التي تطلب Access Token جديداً بصمت
 *   عبر /auth/refresh، والمتصفح يرفق الـ HttpOnly Cookie تلقائياً دون أي كود هنا يراه.
 */
export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    accessToken: null,
    hydrated: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    async register(payload) {
      const { request } = useApi();
      await request("/auth/register", { method: "POST", body: payload });
      return await this.login({ email: payload.email, password: payload.password });
    },

    async login({ email, password }) {
      const { request } = useApi();
      const data = await request("/auth/login", {
        method: "POST",
        body: { email, password },
      });

      this.accessToken = data.access; // Refresh Token غير موجود بهذه الاستجابة أساساً — يُدار عبر Cookie فقط
      await this.fetchMe();
      return data;
    },

    async fetchMe() {
      const { request } = useApi();
      this.user = await request("/account/me");
    },

    /** تُستدعى مرة عند بداية تحميل التطبيق لاستعادة الجلسة بصمت إن وُجدت. */
    async hydrate() {
      if (this.hydrated) return;
      this.hydrated = true;

      const { request } = useApi();
      try {
        const data = await request("/auth/refresh", { method: "POST" });
        this.accessToken = data.access;
        await this.fetchMe();
      } catch {
        this.accessToken = null;
        this.user = null;
      }
    },

    async logout() {
      const { request } = useApi();
      try {
        await request("/auth/logout", { method: "POST" });
      } catch {
        // نكمل تسجيل الخروج محلياً حتى لو فشل الاتصال بالخادم
      }
      this.accessToken = null;
      this.user = null;
      navigateTo("/");
    },
  },
});
