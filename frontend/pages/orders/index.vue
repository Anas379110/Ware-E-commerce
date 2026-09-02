<template>
  <div>
    <h1 style="margin: 0 0 16px;">طلباتي</h1>

    <p v-if="!orders.length" class="text-muted">لا توجد طلبات سابقة بعد.</p>

    <div v-for="order in orders" :key="order.id" class="card" style="margin-bottom: 10px;">
      <NuxtLink :to="`/orders/${order.id}`" style="display: flex; justify-content: space-between; align-items: center;">
        <span>طلب #{{ order.id }}</span>
        <span :class="order.status === 'confirmed' ? 'badge-success' : 'badge-danger'">{{ statusLabel(order.status) }}</span>
        <span style="font-weight: 700;">{{ order.total_amount }} $</span>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ middleware: "auth" });

const { request } = useApi();
const orders = ref([]);

const labels = {
  pending: "قيد الانتظار",
  confirmed: "مؤكَّد",
  shipped: "تم الشحن",
  delivered: "تم التسليم",
  cancelled: "ملغى",
  failed: "فشل الدفع",
};

function statusLabel(status) {
  return labels[status] || status;
}

onMounted(async () => {
  const data = await request("/orders");
  orders.value = data.results || data;
});
</script>
