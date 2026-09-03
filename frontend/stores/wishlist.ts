import { defineStore } from "pinia";

export const useWishlistStore = defineStore("wishlist", {
  state: () => ({
    items: [],
  }),

  getters: {
    productIds: (state) => state.items.map((i) => i.product),
  },

  actions: {
    async fetchWishlist() {
      const { request } = useApi();
      try {
        this.items = await request("/wishlist");
      } catch {
        this.items = [];
      }
    },

    isWishlisted(productId) {
      return this.items.some((i) => i.product === productId);
    },

    async toggle(productId) {
      const { request } = useApi();
      if (this.isWishlisted(productId)) {
        await request(`/wishlist/${productId}`, { method: "DELETE" });
      } else {
        await request("/wishlist", { method: "POST", body: { product: productId } });
      }
      await this.fetchWishlist();
    },
  },
});
