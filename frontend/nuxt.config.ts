// راجع docs/design/UI-UX.md قبل تعديل الألوان أو الهوية أدناه.
export default defineNuxtConfig({
  compatibilityDate: "2026-01-01",
  devtools: { enabled: true },

  modules: ["@pinia/nuxt", "@vite-pwa/nuxt", "@nuxtjs/i18n"],

  i18n: {
    locales: [
      { code: "ar", iso: "ar-SY", name: "العربية", dir: "rtl", file: "ar.json" },
      { code: "en", iso: "en-US", name: "English", dir: "ltr", file: "en.json" },
    ],
    langDir: "locales/",
    defaultLocale: "ar",
    strategy: "no_prefix",
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: "ware_i18n_redirected",
      redirectOn: "root",
    },
  },

  css: ["~/assets/css/main.css"],

  app: {
    head: {
      title: "Ware — المنتجات الصناعية والتجارية السورية",
      meta: [
        { name: "theme-color", content: "#0C447C" },
        { name: "description", content: "منصة Ware للتجارة الإلكترونية — كل المنتجات الصناعية والتجارية السورية." },
      ],
    },
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1",
    },
  },

  pwa: {
    registerType: "autoUpdate",
    manifest: {
      name: "Ware",
      short_name: "Ware",
      description: "منصة Ware للتجارة الإلكترونية السورية",
      theme_color: "#0C447C",
      background_color: "#F1EFE8",
      display: "standalone",
      lang: "ar",
      dir: "rtl",
      icons: [
        { src: "/icons/icon-192.png", sizes: "192x192", type: "image/png" },
        { src: "/icons/icon-512.png", sizes: "512x512", type: "image/png" },
      ],
    },
    workbox: {
      navigateFallback: "/",
      globPatterns: ["**/*.{js,css,html,png,svg,ico}"],
    },
    devOptions: {
      enabled: true,
    },
  },
});
