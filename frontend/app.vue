<template>
  <div>
    <header style="background: var(--color-primary); color: #fff; padding: 14px 0; position: sticky; top: 0; z-index: 50;">
      <div class="container" style="display: flex; align-items: center; justify-content: space-between; gap: 16px;">
        <NuxtLink to="/" style="color: #fff; font-weight: 700; font-size: 20px;">Ware</NuxtLink>

        <form @submit.prevent="goSearch" style="flex: 1; max-width: 420px;">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="ابحث عن منتج..."
            style="width: 100%; padding: 8px 12px; border-radius: 8px; border: none;"
          />
        </form>

        <nav style="display: flex; align-items: center; gap: 14px;">
          <NuxtLink to="/cart" style="color: #fff;">
            السلة ({{ cart.items.length }})
          </NuxtLink>
          <NuxtLink v-if="!auth.isAuthenticated" to="/account/login" style="color: #fff;">دخول</NuxtLink>
          <template v-else>
            <NuxtLink to="/orders" style="color: #fff;">طلباتي</NuxtLink>
            <button @click="auth.logout()" style="background: none; border: none; color: #fff; cursor: pointer; font-family: inherit; font-size: inherit;">
              خروج
            </button>
          </template>
        </nav>
      </div>
    </header>

    <main class="container" style="padding: 24px 16px 60px;">
      <NuxtPage />
    </main>

    <footer style="text-align: center; padding: 24px; color: #6b6b68; font-size: 13px;">
      Ware — منصة التجارة الإلكترونية للمنتجات الصناعية والتجارية السورية
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from "~/stores/auth";
import { useCartStore } from "~/stores/cart";

const auth = useAuthStore();
const cart = useCartStore();
const searchQuery = ref("");
const router = useRouter();

onMounted(async () => {
  await auth.hydrate(); // يستعيد الجلسة بصمت إن وُجدت HttpOnly Cookie صالحة
  cart.fetchCart();
});

function goSearch() {
  router.push({ path: "/", query: { search: searchQuery.value } });
}
</script>
