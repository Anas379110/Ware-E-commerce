<template>
  <div>
    <section
      style="
        background: linear-gradient(135deg, var(--color-primary), #093457);
        color: #fff;
        border-radius: 16px;
        padding: 40px 28px;
        margin-bottom: 28px;
      "
    >
      <h1 style="font-size: 26px; margin: 0 0 8px; font-weight: 800;">{{ $t("home.title") }}</h1>
      <p style="opacity: .9; margin: 0; max-width: 520px;">{{ $t("home.subtitle") }}</p>
    </section>

    <section v-if="categories.length" style="margin-bottom: 28px;">
      <h2 style="font-size: 16px; margin: 0 0 12px; color: var(--color-neutral);">{{ $t("home.categories") }}</h2>
      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(96px, 1fr)); gap: 12px;">
        <button
          class="cat-tile"
          :style="categoryTileStyle(null)"
          @click="selectCategory(null)"
        >
          <LayoutGrid :size="22" />
          <span style="font-size: 12.5px; margin-top: 6px;">{{ $t("home.all") }}</span>
        </button>
        <button
          v-for="cat in categories"
          :key="cat.id"
          class="cat-tile"
          :style="categoryTileStyle(cat.slug)"
          @click="selectCategory(cat.slug)"
        >
          <CategoryIcon :name="cat.icon" :size="22" />
          <span style="font-size: 12.5px; margin-top: 6px;">{{ cat.name }}</span>
        </button>
      </div>
    </section>

    <p v-if="pending" class="text-muted">{{ $t("home.loading") }}</p>
    <p v-else-if="!products.length" class="text-muted">{{ $t("home.empty") }}</p>

    <section v-else style="display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 14px;">
      <ProductCard v-for="product in products" :key="product.id" :product="product" />
    </section>
  </div>
</template>

<script setup>
import { LayoutGrid } from "lucide-vue-next";

const route = useRoute();
const router = useRouter();
const { request } = useApi();

const products = ref([]);
const categories = ref([]);
const pending = ref(true);
const activeCategory = ref(route.query.category || null);

function categoryTileStyle(slug) {
  const active = activeCategory.value === slug;
  return {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    padding: "14px 8px",
    borderRadius: "12px",
    border: active ? "2px solid var(--color-primary)" : "1px solid #e5e2d9",
    background: active ? "#eaf1f7" : "#fff",
    color: active ? "var(--color-primary)" : "var(--color-neutral)",
    cursor: "pointer",
    fontFamily: "inherit",
  };
}

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
