<template>
  <div>
    <h1 style="margin: 0 0 16px;">{{ $t("orders.title") }}</h1>

    <p v-if="!orders.length" class="text-muted">{{ $t("orders.empty") }}</p>

    <div v-for="order in orders" :key="order.id" class="card" style="margin-bottom: 10px;">
      <NuxtLink :to="`/orders/${order.id}`" style="display: flex; justify-content: space-between; align-items: center;">
        <span>#{{ order.id }}</span>
        <span :class="order.status === 'confirmed' ? 'badge-success' : 'badge-danger'">{{ $t(`orders.status.${order.status}`) }}</span>
        <span style="font-weight: 700;">{{ order.total_amount }} $</span>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ middleware: "auth" });

const { request } = useApi();
const orders = ref([]);

onMounted(async () => {
  const data = await request("/orders");
  orders.value = data.results || data;
});
</script>
