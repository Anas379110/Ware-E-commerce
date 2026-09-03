<template>
  <div>
    <h1 style="margin: 0 0 16px;">{{ $t("nav.wishlist") }}</h1>

    <p v-if="!wishlist.items.length" class="text-muted">
      {{ $t("cart.empty") }} <NuxtLink to="/">{{ $t("cart.browse") }}</NuxtLink>
    </p>

    <section v-else style="display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 14px;">
      <ProductCard v-for="item in wishlist.items" :key="item.id" :product="item.product_detail" />
    </section>
  </div>
</template>

<script setup>
definePageMeta({ middleware: "auth" });

const wishlist = useWishlistStore();

onMounted(() => {
  wishlist.fetchWishlist();
});
</script>
