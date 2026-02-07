<template>
  <header
    class="sticky top-0 z-50 w-full bg-white/80 dark:bg-background-dark/80 backdrop-blur-md border-b border-[#f0f2f4] dark:border-gray-800"
  >
    <div
      class="max-w-[1440px] mx-auto px-8 h-20 flex items-center justify-between"
    >
      <!-- Logo -->
      <router-link to="/" class="flex items-center gap-3">
        <div class="text-primary">
          <svg
            class="size-7"
            fill="none"
            viewBox="0 0 48 48"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M6 6H42L36 24L42 42H6L12 24L6 6Z"
              fill="currentColor"
            ></path>
          </svg>
        </div>
        <h1 class="text-xl font-bold tracking-tight">MINIMALIST</h1>
      </router-link>

      <!-- Search -->
      <div class="flex-1 max-w-md mx-12">
        <div class="relative group">
          <span
            class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-lg"
            >search</span
          >
          <input
            class="w-full bg-[#f0f2f4] dark:bg-gray-800 border-none rounded-lg pl-10 pr-4 py-2 text-sm focus:ring-1 focus:ring-primary/30 transition-all placeholder:text-gray-500"
            placeholder="Search our collection..."
            type="text"
            v-model="searchQuery"
            @keyup.enter="handleSearch"
          />
        </div>
      </div>

      <!-- Nav Links & Icons -->
      <nav class="flex items-center gap-10">
        <div
          class="hidden lg:flex items-center gap-8 text-sm font-medium tracking-wide uppercase text-gray-600 dark:text-gray-300"
        >
          <router-link to="/search" class="hover:text-primary transition-colors"
            >Shop</router-link
          >
          <a class="hover:text-primary transition-colors" href="#"
            >Collections</a
          >
          <a class="hover:text-primary transition-colors" href="#">Journal</a>
        </div>
        <div class="h-6 w-px bg-gray-200 dark:bg-gray-700"></div>
        <div class="flex items-center gap-5">
          <router-link
            to="/wishlist"
            class="text-gray-700 dark:text-gray-200 hover:text-primary transition-colors"
          >
            <span class="material-symbols-outlined">favorite</span>
          </router-link>
          <router-link
            to="/login"
            class="text-gray-700 dark:text-gray-200 hover:text-primary transition-colors hover:bg-gray-100 dark:hover:bg-gray-800 p-1 rounded-full group flex items-center gap-1"
          >
            <span class="material-symbols-outlined">person</span>
            <span
              class="text-[10px] font-bold uppercase tracking-tight hidden md:block"
              >Login</span
            >
          </router-link>
          <router-link
            to="/checkout"
            class="relative text-gray-700 dark:text-gray-200 hover:text-primary transition-colors"
          >
            <span class="material-symbols-outlined">shopping_bag</span>
            <span
              v-if="cartCount > 0"
              class="absolute -top-1 -right-1 bg-primary text-white text-[10px] w-4 h-4 rounded-full flex items-center justify-center font-bold"
            >
              {{ cartCount }}
            </span>
          </router-link>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const searchQuery = ref("");
const cartCount = ref(2); // Mocked for now

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ name: "search", query: { q: searchQuery.value } });
  }
};
</script>
