<template>
  <component :is="resolvedIcon" :size="size" />
</template>

<script setup>
import * as icons from "lucide-vue-next";

const props = defineProps({
  name: { type: String, default: "" },
  size: { type: Number, default: 20 },
});

// يحوّل اسم الأيقونة النصي (مثال: "wrench") لاسم مكوّن PascalCase (مثال: "Wrench")
// المطابق لمكتبة lucide-vue-next. يستخدم Package كأيقونة افتراضية إن لم يُحدَّد اسم صالح.
const resolvedIcon = computed(() => {
  if (!props.name) return icons.Package;
  const pascal = props.name
    .split(/[-_\s]/)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join("");
  return icons[pascal] || icons.Package;
});
</script>
