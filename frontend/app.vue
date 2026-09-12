<template>
  <div>
    <header style="background: var(--color-primary); color: #fff; padding: 14px 0; position: sticky; top: 0; z-index: 50;">
      <div class="container" style="display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap;">
        <NuxtLink to="/" style="color: #fff; font-weight: 700; font-size: 20px; display: flex; align-items: center; gap: 6px;">
          <Package :size="22" /> Ware
        </NuxtLink>

        <form @submit.prevent="goSearch" style="flex: 1; max-width: 420px; min-width: 160px;">
          <div style="position: relative;">
            <Search :size="16" style="position: absolute; inset-inline-start: 10px; top: 50%; transform: translateY(-50%); color: #888;" />
            <input
              v-model="searchQuery"
              type="text"
              :placeholder="$t('nav.search_placeholder')"
              style="width: 100%; padding: 8px 12px 8px 34px; border-radius: 8px; border: none;"
            />
          </div>
        </form>

        <nav style="display: flex; align-items: center; gap: 16px;">
          <button
            class="lang-switch"
            style="background: rgba(255,255,255,.15); border: none; color: #fff; border-radius: 6px; padding: 5px 10px; cursor: pointer; font-size: 13px;"
            @click="switchLocale"
          >
            {{ locale === "ar" ? "EN" : "AR" }}
          </button>

          <NuxtLink v-if="auth.isAuthenticated" to="/wishlist" style="color: #fff; display: flex; align-items: center; gap: 4px;">
            <Heart :size="18" />
          </NuxtLink>

          <NuxtLink to="/cart" style="color: #fff; display: flex; align-items: center; gap: 4px;">
            <ShoppingCart :size="18" />
            <span>({{ cart.items.length }})</span>
          </NuxtLink>

          <NuxtLink v-if="!auth.isAuthenticated" to="/account/login" style="color: #fff;">{{ $t("nav.login") }}</NuxtLink>
          <template v-else>
            <NuxtLink to="/orders" style="color: #fff;">{{ $t("nav.orders") }}</NuxtLink>
            <button @click="auth.logout()" style="background: none; border: none; color: #fff; cursor: pointer; font-family: inherit; font-size: inherit;">
              {{ $t("nav.logout") }}
            </button>
          </template>
        </nav>
      </div>
    </header>

    <main class="container" style="padding: 24px 16px 60px;">
      <NuxtPage />
    </main>

    <footer style="text-align: center; padding: 24px; color: #6b6b68; font-size: 13px;">
      {{ $t("footer.tagline") }}
    </footer>
  </div>
</template>

<script setup>
import { Heart, Package, Search, ShoppingCart } from "lucide-vue-next";
import { useAuthStore } from "~/stores/auth";
import { useCartStore } from "~/stores/cart";
import { useWishlistStore } from "~/stores/wishlist";

const auth = useAuthStore();
const cart = useCartStore();
const wishlist = useWishlistStore();
const searchQuery = ref("");
const router = useRouter();

const { locale, setLocale } = useI18n();

useHead({
  htmlAttrs: {
    lang: computed(() => locale.value),
    dir: computed(() => (locale.value === "ar" ? "rtl" : "ltr")),
  },
});

function switchLocale() {
  setLocale(locale.value === "ar" ? "en" : "ar");
}

onMounted(async () => {
  await auth.hydrate(); // يستعيد الجلسة بصمت إن وُجدت HttpOnly Cookie صالحة
  cart.fetchCart();
  if (auth.isAuthenticated) wishlist.fetchWishlist();
});

watch(
  () => auth.isAuthenticated,
  (isAuth) => {
    if (isAuth) wishlist.fetchWishlist();
  }
);

function goSearch() {
  router.push({ path: "/", query: { search: searchQuery.value } });
}
</script>
