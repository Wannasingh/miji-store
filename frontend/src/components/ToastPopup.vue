<template>
  <div
    class="fixed top-4 right-4 z-[100] flex flex-col gap-3 max-w-sm w-full pointer-events-none"
    aria-live="polite"
  >
    <transition-group name="toast">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="pointer-events-auto flex items-start gap-3 px-4 py-3 rounded-xl border shadow-lg backdrop-blur-sm"
        :class="toastClass(t.type)"
        role="alert"
      >
        <span class="material-symbols-outlined shrink-0 mt-0.5" :class="iconClass(t.type)">
          {{ iconName(t.type) }}
        </span>
        <p class="text-sm font-medium flex-1">{{ t.message }}</p>
        <button
          type="button"
          class="shrink-0 p-1 rounded hover:bg-black/10 dark:hover:bg-white/10 transition-colors"
          aria-label="ปิด"
          @click="remove(t.id)"
        >
          <span class="material-symbols-outlined text-lg">close</span>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useToast } from "../composables/useToast.js";

const { toasts, remove } = useToast();

function toastClass(type) {
  const base = "bg-white dark:bg-gray-900";
  const byType = {
    success: "border-green-200 dark:border-green-800 text-gray-900 dark:text-gray-100",
    warning: "border-amber-200 dark:border-amber-800 text-gray-900 dark:text-gray-100",
    error: "border-red-200 dark:border-red-800 text-gray-900 dark:text-gray-100",
    info: "border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100",
  };
  return `${base} ${byType[type] || byType.info}`;
}

function iconClass(type) {
  const byType = {
    success: "text-green-600 dark:text-green-400",
    warning: "text-amber-600 dark:text-amber-400",
    error: "text-red-600 dark:text-red-400",
    info: "text-primary",
  };
  return byType[type] || byType.info;
}

function iconName(type) {
  const names = { success: "check_circle", warning: "warning", error: "error", info: "info" };
  return names[type] || "info";
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
