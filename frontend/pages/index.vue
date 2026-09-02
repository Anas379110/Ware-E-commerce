<template>
  <div>
    <section style="margin-bottom: 24px;">
      <h1 style="font-size: 24px; margin: 0 0 6px;">كل المنتجات الصناعية والتجارية السورية</h1>
      <p class="text-muted">تصفّح، اختر، وادفع بثقة عبر Stripe أو شام كاش.</p>
    </section>

    <section v-if="categories.length" style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px;">
      <button
        class="btn"
        :class="!activeCategory ? 'btn-primary' : ''"
        :style="!activeCategory ? '' : 'background:#fff;border:1px solid #ddd;'"
        @click="selectCategory(null)"
      >
        الكل
      </button>
      <button
        v-for="cat in categories"
        :key="cat.id"
        class="btn"
        :style="activeCategory === cat.slug ? 'background:var(--color-primary);color:#fff;' : 'background:#fff;border:1px solid #ddd;'"
        @click="selectCategory(cat.slug)"
      >
        {{ cat.name }}
      </button>
    </section>

    <p v-if="pending" class="text-muted">جارٍ تحميل المنتجات...</p>
    <p v-else-if="!products.length" class="text-muted">لا توجد منتجات مطابقة — جرّب تصنيفاً أو بحثاً مختلفاً.</p>

    <section v-else style="display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 14px;">
      <ProductCard v-for="product in products" :key="product.id" :product="product" />
    </section>
  </div>
</template>

<script setup>
const route = useRoute();
const router = useRouter();
const { request } = useApi();

const products = ref([]);
const categories = ref([]);
const pending = ref(true);
const activeCategory = ref(route.query.category || null);

async function loadCategories() {
  categories.value = await request("/categories");
}

async function loadProducts() {
  pending.value = true;
  try {
    const params = {};
    if (route.query.search) params.search = route.query.search;
    if (activeCategory.value) params.category = activeCategory.value;
    const data = await request("/products", { params });
    products.value = data.results || data;
  } finally {
    pending.value = false;
  }
}

function selectCategory(slug) {
  activeCategory.value = slug;
  router.push({ path: "/", query: { ...route.query, category: slug || undefined } });
}

watch(() => route.query, loadProducts, { deep: true });

onMounted(() => {
  loadCategories();
  loadProducts();
});
</script>
