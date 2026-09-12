<template>
  <div class="card" style="position: relative; padding: 0; overflow: hidden;">
    <button
      v-if="auth.isAuthenticated"
      class="wishlist-btn"
      :aria-label="$t('product.add_to_wishlist')"
      style="position: absolute; top: 8px; inset-inline-end: 8px; z-index: 2; background: #fff; border: none; border-radius: 999px; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 1px 4px rgba(0,0,0,.15);"
      @click.prevent="toggleWishlist"
    >
      <Heart :size="15" :fill="isWishlisted ? 'var(--color-danger)' : 'none'" :color="isWishlisted ? 'var(--color-danger)' : '#888'" />
    </button>

    <NuxtLink :to="`/products/${product.slug}`" style="display: block; text-decoration: none; color: inherit; padding: 12px;">
      <div style="width: 100%; aspect-ratio: 1; background: #eee; border-radius: 8px; overflow: hidden; margin-bottom: 10px;">
        <img
          v-if="product.primary_image_url"
          :src="product.primary_image_url"
          :alt="product.name"
          style="width: 100%; height: 100%; object-fit: cover;"
        />
      </div>
      <p style="font-weight: 600; margin: 0 0 4px; font-size: 14.5px;">{{ product.name }}</p>
      <RatingStars :rating="product.average_rating" :count="product.review_count" :size="12" />
      <p style="color: var(--color-primary); font-weight: 700; margin: 6px 0 0;">{{ product.price }} $</p>
      <span v-if="!product.in_stock" class="badge-danger" style="margin-top: 6px; display: inline-block;">
        {{ $t("product.out_of_stock") }}
      </span>
    </NuxtLink>
  </div>
</template>

<script setup>
import { Heart } from "lucide-vue-next";
import { useAuthStore } from "~/stores/auth";
import { useWishlistStore } from "~/stores/wishlist";

const props = defineProps({
  product: { type: Object, required: true },
});

const auth = useAuthStore();
const wishlist = useWishlistStore();

const isWishlisted = computed(() => wishlist.isWishlisted(props.product.id));

function toggleWishlist() {
  wishlist.toggle(props.product.id);
}
</script>
