<template>
  <div v-if="order">
    <h1 style="margin: 0 0 8px;">طلب #{{ order.id }}</h1>
    <span :class="order.status === 'confirmed' ? 'badge-success' : 'badge-danger'">{{ statusLabel(order.status) }}</span>

    <p v-if="route.query.status === 'success'" class="text-muted" style="margin-top: 10px;">
      تم توجيهك من بوابة الدفع بنجاح. ستتحدّث حالة الطلب هنا تلقائياً فور تأكيد البوابة نهائياً (قد يستغرق ذلك لحظات قليلة).
    </p>
    <p v-else-if="route.query.status === 'cancelled'" style="color: var(--color-danger); margin-top: 10px;">
      تم إلغاء عملية الدفع. يمكنك المحاولة مجدداً من صفحة السلة.
    </p>

    <div class="card" style="margin-top: 16px;">
      <div v-for="item in order.items" :key="item.id" style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #eee;">
        <span>{{ item.product_name_snapshot }} × {{ item.quantity }}</span>
        <span>{{ item.subtotal }} $</span>
      </div>
      <div style="display: flex; justify-content: space-between; padding-top: 12px; font-weight: 700;">
        <span>الإجمالي</span>
        <span>{{ order.total_amount }} $</span>
      </div>
    </div>
  </div>
  <p v-else class="text-muted">جارٍ التحميل...</p>
</template>

<script setup>
definePageMeta({ middleware: "auth" });

const route = useRoute();
const { request } = useApi();
const order = ref(null);

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
  order.value = await request(`/orders/${route.params.id}`);
});
</script>
