<template>
  <div>
    <h1 style="margin: 0 0 16px;">{{ $t("checkout.title") }}</h1>

    <section class="card" style="margin-bottom: 16px;">
      <h2 style="font-size: 16px; margin: 0 0 10px;">{{ $t("checkout.address_section") }}</h2>

      <div v-if="addresses.length" style="margin-bottom: 12px;">
        <label v-for="addr in addresses" :key="addr.id" style="display: block; margin-bottom: 8px;">
          <input type="radio" v-model="selectedAddressId" :value="addr.id" />
          {{ addr.full_name }} — {{ addr.city }} — {{ addr.street_details }}
        </label>
      </div>
      <p v-else class="text-muted">{{ $t("checkout.no_address") }}</p>

      <details>
        <summary style="cursor: pointer; color: var(--color-primary);">{{ $t("checkout.add_address") }}</summary>
        <form style="display: grid; gap: 8px; margin-top: 10px; max-width: 400px;" @submit.prevent="saveAddress">
          <input v-model="newAddress.full_name" :placeholder="$t('checkout.full_name')" required style="padding: 8px; border-radius: 8px; border: 1px solid #ddd;" />
          <input v-model="newAddress.phone" :placeholder="$t('checkout.phone')" required style="padding: 8px; border-radius: 8px; border: 1px solid #ddd;" />
          <input v-model="newAddress.city" :placeholder="$t('checkout.city')" required style="padding: 8px; border-radius: 8px; border: 1px solid #ddd;" />
          <textarea v-model="newAddress.street_details" :placeholder="$t('checkout.street_details')" required style="padding: 8px; border-radius: 8px; border: 1px solid #ddd;"></textarea>
          <button type="submit" class="btn btn-primary" style="width: fit-content;">{{ $t("checkout.save_address") }}</button>
        </form>
      </details>
    </section>

    <section class="card" style="margin-bottom: 16px;">
      <h2 style="font-size: 16px; margin: 0 0 10px;">{{ $t("checkout.coupon_section") }}</h2>
      <div style="display: flex; gap: 8px;">
        <input
          v-model="couponCode"
          :placeholder="$t('checkout.coupon_placeholder')"
          style="flex: 1; padding: 8px; border-radius: 8px; border: 1px solid #ddd; text-transform: uppercase;"
        />
        <button class="btn btn-primary" type="button" :disabled="!couponCode || applyingCoupon" @click="applyCoupon">
          {{ $t("checkout.apply_coupon") }}
        </button>
      </div>
      <p v-if="couponResult" class="text-muted" style="margin-top: 8px; color: var(--color-success);">
        {{ $t("checkout.coupon_applied") }}: -{{ couponResult.discount }} $
      </p>
      <p v-if="couponError" style="color: var(--color-danger); margin-top: 8px;">{{ couponError }}</p>
    </section>

    <section class="card" style="margin-bottom: 16px;">
      <h2 style="font-size: 16px; margin: 0 0 10px;">{{ $t("checkout.payment_section") }}</h2>
      <label style="display: block; margin-bottom: 8px;">
        <input type="radio" v-model="paymentMethod" value="stripe" /> {{ $t("checkout.stripe") }}
      </label>
      <label style="display: block;">
        <input type="radio" v-model="paymentMethod" value="sham_cash" /> {{ $t("checkout.sham_cash") }}
      </label>
    </section>

    <div class="card" style="margin-bottom: 16px;">
      <div style="display: flex; justify-content: space-between; font-size: 14px; color: var(--color-neutral); margin-bottom: 4px;">
        <span>{{ $t("checkout.subtotal") }}</span>
        <span>{{ cart.total }} $</span>
      </div>
      <div v-if="couponResult" style="display: flex; justify-content: space-between; font-size: 14px; color: var(--color-success); margin-bottom: 4px;">
        <span>{{ $t("checkout.discount") }}</span>
        <span>-{{ couponResult.discount }} $</span>
      </div>
      <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 17px; margin-top: 8px; border-top: 1px solid #eee; padding-top: 8px;">
        <span>{{ $t("cart.total") }}</span>
        <span>{{ estimatedTotal }} $</span>
      </div>
    </div>

    <p v-if="error" style="color: var(--color-danger);">{{ error }}</p>

    <button class="btn btn-accent" :disabled="!selectedAddressId || submitting" @click="submitOrder">
      {{ submitting ? $t("checkout.processing") : `${$t("checkout.pay_now")} — ${estimatedTotal} $` }}
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

const couponCode = ref("");
const couponResult = ref(null);
const couponError = ref("");
const applyingCoupon = ref(false);

const newAddress = reactive({ full_name: "", phone: "", city: "", street_details: "" });

const estimatedTotal = computed(() => {
  const total = Number(cart.total) - Number(couponResult.value?.discount || 0);
  return total.toFixed(2);
});

async function loadAddresses() {
  addresses.value = await request("/account/addresses");
  if (addresses.value.length) selectedAddressId.value = addresses.value[0].id;
}

async function saveAddress() {
  const created = await request("/account/addresses", { method: "POST", body: newAddress });
  addresses.value.push(created);
  selectedAddressId.value = created.id;
}

async function applyCoupon() {
  applyingCoupon.value = true;
  couponError.value = "";
  couponResult.value = null;
  try {
    couponResult.value = await request("/promotions/validate-coupon", {
      method: "POST",
      body: { code: couponCode.value },
    });
  } catch (e) {
    couponError.value = e?.data?.error || "—";
  } finally {
    applyingCoupon.value = false;
  }
}

async function submitOrder() {
  submitting.value = true;
  error.value = "";
  try {
    const body = { address_id: selectedAddressId.value };
    if (couponResult.value) body.coupon_code = couponCode.value.trim().toUpperCase();

    const order = await request("/checkout", { method: "POST", body });

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
    error.value = e?.data?.error || "—";
  } finally {
    submitting.value = false;
  }
}

onMounted(loadAddresses);
</script>
