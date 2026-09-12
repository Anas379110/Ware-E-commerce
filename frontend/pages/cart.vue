<template>
  <div>
    <h1 style="margin: 0 0 16px;">{{ $t("cart.title") }}</h1>

    <p v-if="!cart.items.length" class="text-muted">
      {{ $t("cart.empty") }} <NuxtLink to="/">{{ $t("cart.browse") }}</NuxtLink>
    </p>

    <div v-else>
      <div v-for="item in cart.items" :key="item.id" class="card" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 10px;">
        <div>
          <p style="font-weight: 600; margin: 0;">{{ item.product_name }}</p>
          <p class="text-muted" style="margin: 4px 0 0;">{{ item.unit_price }} $ {{ $t("cart.each") }}</p>
        </div>

        <div style="display: flex; align-items: center; gap: 10px;">
          <input
            type="number"
            min="1"
            :value="item.quantity"
            style="width: 60px; padding: 6px; border-radius: 8px; border: 1px solid #ddd;"
            @change="onQuantityChange(item, $event)"
          />
          <p style="width: 80px; text-align: left; font-weight: 700; margin: 0;">{{ item.subtotal }} $</p>
          <button class="btn" style="background: #fdecea; color: var(--color-danger);" @click="cart.removeItem(item.id)">
            {{ $t("cart.remove") }}
          </button>
        </div>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
        <p style="font-size: 18px; font-weight: 700;">{{ $t("cart.total") }}: {{ cart.total }} $</p>
        <NuxtLink to="/checkout" class="btn btn-accent">{{ $t("cart.checkout") }}</NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
const cart = useCartStore();

onMounted(() => {
  cart.fetchCart();
});

function onQuantityChange(item, event) {
  const value = Number(event.target.value);
  if (value > 0) cart.updateItem(item.id, value);
}
</script>
