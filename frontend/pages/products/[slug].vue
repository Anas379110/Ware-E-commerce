<template>
  <div v-if="product">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
      <div style="background: #eee; border-radius: var(--radius); aspect-ratio: 1; overflow: hidden;">
        <img
          v-if="product.primary_image_url"
          :src="product.primary_image_url"
          :alt="product.name"
          style="width: 100%; height: 100%; object-fit: cover;"
        />
      </div>

      <div>
        <h1 style="margin: 0 0 8px;">{{ product.name }}</h1>
        <p style="font-size: 22px; font-weight: 700; color: var(--color-primary); margin: 0 0 12px;">
          {{ product.price }} $
        </p>
        <span v-if="product.in_stock" class="badge-success">متوفر</span>
        <span v-else class="badge-danger">غير متوفر حالياً</span>

        <p style="margin: 16px 0; line-height: 1.8;">{{ product.description }}</p>

        <div style="display: flex; align-items: center; gap: 10px; margin: 16px 0;">
          <input v-model.number="quantity" type="number" min="1" :max="product.stock_quantity" style="width: 70px; padding: 8px; border-radius: 8px; border: 1px solid #ddd;" />
          <button class="btn btn-accent" :disabled="!product.in_stock || adding" @click="addToCart">
            {{ adding ? "جارٍ الإضافة..." : "أضف للسلة" }}
          </button>
        </div>

        <p v-if="message" class="text-muted">{{ message }}</p>
      </div>
    </div>
  </div>
  <p v-else class="text-muted">جارٍ التحميل...</p>
</template>

<script setup>
const route = useRoute();
const { request } = useApi();
const cart = useCartStore();

const product = ref(null);
const quantity = ref(1);
const adding = ref(false);
const message = ref("");

async function loadProduct() {
  product.value = await request(`/products/${route.params.slug}`);
}

async function addToCart() {
  adding.value = true;
  message.value = "";
  try {
    await cart.addItem(product.value.id, quantity.value);
    message.value = "تمت الإضافة للسلة.";
  } catch (e) {
    message.value = e?.data?.error || "تعذّرت إضافة المنتج — تحقق من الكمية المتوفرة.";
  } finally {
    adding.value = false;
  }
}

onMounted(loadProduct);
</script>
