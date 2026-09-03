<template>
  <div v-if="product">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
      <div style="background: #eee; border-radius: var(--radius); aspect-ratio: 1; overflow: hidden; position: relative;">
        <img
          v-if="product.primary_image_url"
          :src="product.primary_image_url"
          :alt="product.name"
          style="width: 100%; height: 100%; object-fit: cover;"
        />
        <button
          v-if="auth.isAuthenticated"
          style="position: absolute; top: 10px; inset-inline-end: 10px; background: #fff; border: none; border-radius: 999px; width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 1px 4px rgba(0,0,0,.15);"
          :aria-label="$t('product.add_to_wishlist')"
          @click="wishlist.toggle(product.id)"
        >
          <Heart :size="18" :fill="isWishlisted ? 'var(--color-danger)' : 'none'" :color="isWishlisted ? 'var(--color-danger)' : '#888'" />
        </button>
      </div>

      <div>
        <h1 style="margin: 0 0 6px;">{{ product.name }}</h1>
        <RatingStars :rating="product.average_rating" :count="product.review_count" />
        <p style="font-size: 22px; font-weight: 700; color: var(--color-primary); margin: 10px 0 12px;">
          {{ product.price }} $
        </p>
        <span v-if="product.in_stock" class="badge-success">{{ $t("product.in_stock") }}</span>
        <span v-else class="badge-danger">{{ $t("product.out_of_stock") }}</span>

        <p style="margin: 16px 0; line-height: 1.8;">{{ product.description }}</p>

        <div style="display: flex; align-items: center; gap: 10px; margin: 16px 0;">
          <input v-model.number="quantity" type="number" min="1" :max="product.stock_quantity" style="width: 70px; padding: 8px; border-radius: 8px; border: 1px solid #ddd;" />
          <button class="btn btn-accent" :disabled="!product.in_stock || adding" @click="addToCart">
            {{ adding ? $t("product.adding") : $t("product.add_to_cart") }}
          </button>
        </div>

        <p v-if="message" class="text-muted">{{ message }}</p>
      </div>
    </div>

    <!-- منتجات ذات صلة -->
    <section v-if="product.related_products?.length" style="margin-top: 40px;">
      <h2 style="font-size: 17px; margin: 0 0 14px;">{{ $t("product.related") }}</h2>
      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 14px;">
        <ProductCard v-for="rp in product.related_products" :key="rp.id" :product="rp" />
      </div>
    </section>

    <!-- التقييمات -->
    <section style="margin-top: 40px; max-width: 640px;">
      <h2 style="font-size: 17px; margin: 0 0 14px;">{{ $t("product.reviews") }}</h2>

      <p v-if="!reviews.length" class="text-muted">{{ $t("product.no_reviews") }}</p>
      <div v-for="review in reviews" :key="review.id" class="card" style="margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <strong style="font-size: 13.5px;">{{ review.user_name || "—" }}</strong>
          <RatingStars :rating="review.rating" :show-count="false" :size="13" />
        </div>
        <p v-if="review.comment" style="margin: 8px 0 0; font-size: 14px; color: var(--color-neutral);">
          {{ review.comment }}
        </p>
      </div>

      <div v-if="auth.isAuthenticated" class="card" style="margin-top: 16px;">
        <h3 style="font-size: 14.5px; margin: 0 0 10px;">{{ $t("product.add_review") }}</h3>
        <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 10px;">
          <button
            v-for="n in 5"
            :key="n"
            type="button"
            style="background: none; border: none; cursor: pointer; padding: 0;"
            @click="newReview.rating = n"
          >
            <Star :size="20" :fill="n <= newReview.rating ? 'var(--color-accent)' : 'none'" :color="n <= newReview.rating ? 'var(--color-accent)' : '#ccc'" />
          </button>
        </div>
        <textarea
          v-model="newReview.comment"
          :placeholder="$t('product.comment')"
          style="width: 100%; padding: 8px; border-radius: 8px; border: 1px solid #ddd; margin-bottom: 10px; font-family: inherit;"
        ></textarea>
        <button class="btn btn-primary" :disabled="!newReview.rating || submittingReview" @click="submitReview">
          {{ $t("product.submit_review") }}
        </button>
        <p v-if="reviewError" style="color: var(--color-danger); margin-top: 8px;">{{ reviewError }}</p>
      </div>
    </section>
  </div>
  <p v-else class="text-muted">...</p>
</template>

<script setup>
import { Heart, Star } from "lucide-vue-next";
import { useAuthStore } from "~/stores/auth";
import { useWishlistStore } from "~/stores/wishlist";

const route = useRoute();
const { request } = useApi();
const cart = useCartStore();
const auth = useAuthStore();
const wishlist = useWishlistStore();
const { t } = useI18n();

const product = ref(null);
const reviews = ref([]);
const quantity = ref(1);
const adding = ref(false);
const message = ref("");
const submittingReview = ref(false);
const reviewError = ref("");
const newReview = reactive({ rating: 0, comment: "" });

const isWishlisted = computed(() => product.value && wishlist.isWishlisted(product.value.id));

async function loadProduct() {
  product.value = await request(`/products/${route.params.slug}`);
}

async function loadReviews() {
  reviews.value = await request(`/products/${route.params.slug}/reviews`);
}

async function addToCart() {
  adding.value = true;
  message.value = "";
  try {
    await cart.addItem(product.value.id, quantity.value);
    message.value = t("product.added");
  } catch (e) {
    message.value = e?.data?.error || t("product.add_failed");
  } finally {
    adding.value = false;
  }
}

async function submitReview() {
  submittingReview.value = true;
  reviewError.value = "";
  try {
    await request(`/products/${route.params.slug}/reviews`, {
      method: "POST",
      body: { rating: newReview.rating, comment: newReview.comment },
    });
    newReview.rating = 0;
    newReview.comment = "";
    await loadReviews();
    await loadProduct();
  } catch (e) {
    reviewError.value = e?.data?.error || t("product.add_failed");
  } finally {
    submittingReview.value = false;
  }
}

onMounted(async () => {
  await loadProduct();
  await loadReviews();
});
</script>
