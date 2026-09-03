<template>
  <div v-if="order">
    <h1 style="margin: 0 0 8px;">#{{ order.id }}</h1>
    <span :class="order.status === 'confirmed' ? 'badge-success' : 'badge-danger'">{{ $t(`orders.status.${order.status}`) }}</span>

    <p v-if="route.query.status === 'success'" class="text-muted" style="margin-top: 10px;">
      {{ $t("checkout.processing") }}
    </p>

    <div class="card" style="margin-top: 16px;">
      <div v-for="item in order.items" :key="item.id" style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
        <span>{{ item.product_name_snapshot }} × {{ item.quantity }}</span>
        <span>{{ item.subtotal }} $</span>
      </div>

      <div style="display: flex; justify-content: space-between; padding-top: 10px; font-size: 14px; color: var(--color-neutral);">
        <span>{{ $t("checkout.subtotal") }}</span>
        <span>{{ order.subtotal }} $</span>
      </div>
      <div v-if="Number(order.discount_amount) > 0" style="display: flex; justify-content: space-between; font-size: 14px; color: var(--color-success);">
        <span>{{ $t("checkout.discount") }} ({{ order.coupon_code }})</span>
        <span>-{{ order.discount_amount }} $</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding-top: 8px; border-top: 1px solid #eee; font-weight: 700;">
        <span>{{ $t("cart.total") }}</span>
        <span>{{ order.total_amount }} $</span>
      </div>
    </div>
  </div>
  <p v-else class="text-muted">...</p>
</template>

<script setup>
definePageMeta({ middleware: "auth" });

const route = useRoute();
const { request } = useApi();
const order = ref(null);

onMounted(async () => {
  order.value = await request(`/orders/${route.params.id}`);
});
</script>
