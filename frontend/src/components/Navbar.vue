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
          <router-link class="hover:text-primary transition-colors" to="/search"
            >Collections</router-link
          >
          <router-link class="hover:text-primary transition-colors" to="/search"
            >Journal</router-link
          >
        </div>
        <div class="h-6 w-px bg-gray-200 dark:bg-gray-700"></div>
        <div class="flex items-center gap-5">
          <router-link
            to="/wishlist"
            class="text-gray-700 dark:text-gray-200 hover:text-primary transition-colors"
            title="Wishlist"
          >
            <span class="material-symbols-outlined">favorite</span>
          </router-link>
          <template v-if="isLoggedIn">
            <div class="relative" ref="profileWrapRef">
              <button
                type="button"
                @click="profileMenuOpen = !profileMenuOpen"
                class="flex items-center justify-center w-9 h-9 rounded-full bg-[#f0f2f4] dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-primary/10 hover:text-primary transition-colors border-2 border-transparent focus:border-primary/50 outline-none"
                :class="{ 'ring-2 ring-primary/30': profileMenuOpen }"
                title="เมนูบัญชี"
                aria-haspopup="true"
                :aria-expanded="profileMenuOpen"
              >
                <span class="material-symbols-outlined text-xl">person</span>
              </button>
              <Transition
                enter-active-class="transition ease-out duration-150"
                enter-from-class="opacity-0 -translate-y-1"
                enter-to-class="opacity-100 translate-y-0"
                leave-active-class="transition ease-in duration-100"
                leave-from-class="opacity-100 translate-y-0"
                leave-to-class="opacity-0 -translate-y-1"
              >
                <div
                  v-show="profileMenuOpen"
                  class="absolute right-0 top-full mt-2 w-52 py-1 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 shadow-lg z-[100]"
                  role="menu"
                >
                  <div class="px-4 py-2 border-b border-gray-100 dark:border-gray-700">
                    <p class="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wider">บัญชีของฉัน</p>
                  </div>
                  <router-link
                    to="/profile"
                    @click="profileMenuOpen = false"
                    class="flex items-center gap-2 px-4 py-2.5 text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    role="menuitem"
                  >
                    <span class="material-symbols-outlined text-lg">person</span>
                    โปรไฟล์
                  </router-link>
                  <button
                    type="button"
                    @click="handleLogout"
                    class="flex w-full items-center gap-2 px-4 py-2.5 text-sm text-left text-gray-700 dark:text-gray-200 hover:bg-red-50 dark:hover:bg-red-900/20 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                    role="menuitem"
                  >
                    <span class="material-symbols-outlined text-lg">logout</span>
                    ออกจากระบบ
                  </button>
                </div>
              </Transition>
            </div>
          </template>
          <template v-else>
            <router-link
              to="/login"
              class="text-gray-700 dark:text-gray-200 hover:text-primary transition-colors hover:bg-gray-100 dark:hover:bg-gray-800 p-1 rounded-full group flex items-center gap-1"
              title="เข้าสู่ระบบ"
            >
              <span class="material-symbols-outlined">person</span>
              <span
                class="text-[10px] font-bold uppercase tracking-tight hidden md:block"
                >Login</span
              >
            </router-link>
            <router-link
              to="/signup"
              class="text-gray-700 dark:text-gray-200 hover:text-primary transition-colors hover:bg-gray-100 dark:hover:bg-gray-800 px-2 py-1 rounded-full group flex items-center gap-1 text-sm font-medium"
              title="สมัครสมาชิก"
            >
              <span
                class="text-[10px] font-bold uppercase tracking-tight hidden md:block"
                >Sign up</span
              >
            </router-link>
          </template>
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
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { authState, clearToken, refreshAuthState } from "../utils/auth.js";
import { useToast } from "../composables/useToast.js";

const router = useRouter();
const searchQuery = ref("");
const cartCount = ref(2); // Mocked for now
const profileMenuOpen = ref(false);
const profileWrapRef = ref(null);

const isLoggedIn = computed(() => authState.value);

function onClickOutside(e) {
  if (profileWrapRef.value && !profileWrapRef.value.contains(e.target)) {
    profileMenuOpen.value = false;
  }
}

onMounted(() => {
  refreshAuthState();
  document.addEventListener("click", onClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", onClickOutside);
});

function handleLogout() {
  profileMenuOpen.value = false;
  clearToken();
  useToast().show("ออกจากระบบแล้ว", "success");
  router.push("/");
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ name: "search", query: { q: searchQuery.value } });
  }
};
</script>
