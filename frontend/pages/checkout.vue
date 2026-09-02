<template>
  <div>
    <h1 style="margin: 0 0 16px;">إتمام الشراء</h1>

    <section class="card" style="margin-bottom: 16px;">
      <h2 style="font-size: 16px; margin: 0 0 10px;">عنوان الشحن</h2>

      <div v-if="addresses.length" style="margin-bottom: 12px;">
        <label v-for="addr in addresses" :key="addr.id" style="display: block; margin-bottom: 8px;">
          <input type="radio" v-model="selectedAddressId" :value="addr.id" />
          {{ addr.full_name }} — {{ addr.city }} — {{ addr.street_details }}
        </label>
      </div>
      <p v-else class="text-muted">لا يوجد عنوان محفوظ بعد — أضف عنواناً جديداً بالأسفل.</p>

      <details>
        <summary style="cursor: pointer; color: var(--color-primary);">إضافة عنوان جديد</summary>
        <form style="display: grid; gap: 8px; margin-top: 10px; max-width: 400px;" @submit.prevent="saveAddress">
          <input v-model="newAddress.full_name" placeholder="الاسم الكامل" required style="padding: 8px; border-radius: 8px; border: 1px solid #ddd;" />
          <input v-model="newAddress.phone" placeholder="رقم الهاتف" required style="padding: 8px; border-radius: 8px; border: 1px solid #ddd;" />
          <input v-model="newAddress.city" placeholder="المدينة" required style="padding: 8px; border-radius: 8px; border: 1px solid #ddd;" />
          <textarea v-model="newAddress.street_details" placeholder="تفاصيل العنوان" required style="padding: 8px; border-radius: 8px; border: 1px solid #ddd;"></textarea>
          <button type="submit" class="btn btn-primary" style="width: fit-content;">حفظ العنوان</button>
        </form>
      </details>
    </section>

    <section class="card" style="margin-bottom: 16px;">
      <h2 style="font-size: 16px; margin: 0 0 10px;">وسيلة الدفع</h2>
      <label style="display: block; margin-bottom: 8px;">
        <input type="radio" v-model="paymentMethod" value="stripe" /> بطاقة ائتمانية (Stripe)
      </label>
      <label style="display: block;">
        <input type="radio" v-model="paymentMethod" value="sham_cash" /> شام كاش
      </label>
    </section>

    <p v-if="error" style="color: var(--color-danger);">{{ error }}</p>

    <button class="btn btn-accent" :disabled="!selectedAddressId || submitting" @click="submitOrder">
      {{ submitting ? "جارٍ المعالجة..." : `ادفع الآن — ${cart.total} $` }}
    </button>
  </div>
</template>

<script setup>
definePageMeta({ middleware: "auth" });

const { request } = useApi();
const cart = useCartStore();
const router = useRouter();

const addresses = ref([]);
const selectedAddressId = ref(null);
const paymentMethod = ref("stripe");
const submitting = ref(false);
const error = ref("");

const newAddress = reactive({ full_name: "", phone: "", city: "", street_details: "" });

async function loadAddresses() {
  addresses.value = await request("/account/addresses");
  if (addresses.value.length) selectedAddressId.value = addresses.value[0].id;
}

async function saveAddress() {
  const created = await request("/account/addresses", { method: "POST", body: newAddress });
  addresses.value.push(created);
  selectedAddressId.value = created.id;
}

async function submitOrder() {
  submitting.value = true;
  error.value = "";
  try {
    const order = await request("/checkout", {
      method: "POST",
      body: { address_id: selectedAddressId.value },
    });

    if (paymentMethod.value === "stripe") {
      const session = await request("/payments/stripe/create-session", {
        method: "POST",
        body: { order_id: order.id },
      });
      window.location.href = session.checkout_url;
    } else {
      await request("/payments/sham-cash/initiate", {
        method: "POST",
        body: { order_id: order.id },
      });
      router.push(`/orders/${order.id}`);
    }
  } catch (e) {
    error.value = e?.data?.error || "تعذّر إتمام الطلب — حاول مجدداً.";
  } finally {
    submitting.value = false;
  }
}

onMounted(loadAddresses);
</script>
