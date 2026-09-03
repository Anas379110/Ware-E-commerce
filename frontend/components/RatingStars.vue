<template>
  <span style="display: inline-flex; align-items: center; gap: 2px;">
    <Star
      v-for="n in 5"
      :key="n"
      :size="size"
      :fill="n <= Math.round(rating || 0) ? 'var(--color-accent)' : 'none'"
      :color="n <= Math.round(rating || 0) ? 'var(--color-accent)' : '#ccc'"
    />
    <span v-if="showCount" class="text-muted" style="margin-inline-start: 4px; font-size: 12px;">
      ({{ count || 0 }})
    </span>
  </span>
</template>

<script setup>
import { Star } from "lucide-vue-next";

defineProps({
  rating: { type: [Number, null], default: 0 },
  count: { type: Number, default: 0 },
  size: { type: Number, default: 14 },
  showCount: { type: Boolean, default: true },
});
</script>
