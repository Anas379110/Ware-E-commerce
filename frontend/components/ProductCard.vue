<template>
  <NuxtLink :to="`/products/${product.slug}`" class="card" style="display: block; text-decoration: none; color: inherit;">
    <div
      style="
        width: 100%;
        aspect-ratio: 1;
        background: #eee;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 10px;
      "
    >
      <img
        v-if="product.primary_image_url"
        :src="product.primary_image_url"
        :alt="product.name"
        style="width: 100%; height: 100%; object-fit: cover;"
      />
    </div>
    <p style="font-weight: 600; margin: 0 0 4px; font-size: 14.5px;">{{ product.name }}</p>
    <p style="color: var(--color-primary); font-weight: 700; margin: 0;">{{ product.price }} $</p>
    <span v-if="!product.in_stock" class="badge-danger" style="margin-top: 6px; display: inline-block;">
      غير متوفر حالياً
    </span>
  </NuxtLink>
</template>

<script setup>
defineProps({
  product: { type: Object, required: true },
});
</script>
