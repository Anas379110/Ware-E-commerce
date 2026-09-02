import { defineStore } from "pinia";

export const useCartStore = defineStore("cart", {
  state: () => ({
    id: null,
    items: [],
    total: 0,
    loading: false,
  }),

  actions: {
    async fetchCart() {
      const { request } = useApi();
      this.loading = true;
      try {
        const data = await request("/cart");
        this.id = data.id;
        this.items = data.items;
        this.total = data.total;
      } finally {
        this.loading = false;
      }
    },

    async addItem(productId, quantity = 1) {
      const { request } = useApi();
      await request("/cart/items", {
        method: "POST",
        body: { product: productId, quantity },
      });
      await this.fetchCart();
    },

    async updateItem(itemId, quantity) {
      const { request } = useApi();
      await request(`/cart/items/${itemId}`, {
        method: "PATCH",
        body: { quantity },
      });
      await this.fetchCart();
    },

    async removeItem(itemId) {
      const { request } = useApi();
      await request(`/cart/items/${itemId}`, { method: "DELETE" });
      await this.fetchCart();
    },
  },
});
