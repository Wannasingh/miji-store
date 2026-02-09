<template>
  <div
    v-if="loading"
    class="max-w-[1440px] mx-auto px-6 lg:px-12 py-24 text-center"
  >
    <p class="text-gray-500 animate-pulse">Loading product details...</p>
  </div>

  <main v-else-if="product" class="max-w-[1440px] mx-auto px-6 lg:px-12 py-8">
    <!-- Breadcrumbs -->
    <nav
      class="flex items-center gap-2 text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-widest mb-10"
    >
      <router-link to="/" class="hover:text-primary">Home</router-link>
      <span class="material-symbols-outlined text-[10px]">chevron_right</span>
      <span class="hover:text-primary cursor-pointer">{{
        product.categories?.name || "Shop"
      }}</span>
      <span class="material-symbols-outlined text-[10px]">chevron_right</span>
      <span class="text-gray-900 dark:text-gray-100">{{ product.name }}</span>
    </nav>

    <div class="flex flex-col lg:flex-row gap-16">
      <!-- Left: Gallery Section -->
      <div class="flex-1 space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            class="aspect-[4/5] bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden md:col-span-2"
          >
            <img
              :src="mainImage"
              class="w-full h-full object-cover"
              :alt="product.name"
            />
          </div>
          <div
            v-for="(img, idx) in productImages"
            :key="idx"
            class="aspect-[4/5] bg-gray-100 dark:bg-gray-800 rounded-lg overflow-hidden cursor-pointer hover:opacity-80 transition-opacity"
            @click="setMainImage(img.image_url)"
          >
            <img
              :src="img.image_url"
              class="w-full h-full object-cover"
              loading="lazy"
            />
          </div>
        </div>
      </div>

      <!-- Right: Product Information Panel -->
      <div class="lg:w-[420px]">
        <div class="lg:sticky lg:top-24 space-y-10">
          <!-- Title & Price -->
          <div class="space-y-4">
            <div class="space-y-1">
              <span
                v-if="product.is_limited_edition"
                class="text-xs font-bold text-primary uppercase tracking-widest"
                >Limited Edition</span
              >
              <h1
                class="text-4xl font-black tracking-tight leading-none uppercase"
              >
                {{ product.name }}
              </h1>
            </div>
            <p class="text-2xl font-light">${{ product.price }}</p>
            <p
              class="text-gray-600 dark:text-gray-400 text-sm leading-relaxed max-w-sm"
            >
              {{ product.description }}
            </p>
          </div>

          <!-- Color Selector -->
          <div v-if="uniqueColors.length" class="space-y-4">
            <span
              class="text-xs font-bold uppercase tracking-widest text-gray-400"
              >Color / {{ selectedColor }}</span
            >
            <div class="flex gap-4">
              <label
                v-for="color in uniqueColors"
                :key="color.name"
                class="cursor-pointer"
              >
                <input
                  type="radio"
                  name="color"
                  class="sr-only peer"
                  :value="color.name"
                  v-model="selectedColor"
                />
                <div
                  class="w-8 h-8 rounded-full border-2 border-transparent ring-1 ring-offset-2 ring-transparent peer-checked:ring-primary peer-checked:border-white dark:peer-checked:border-gray-900 transition-all"
                  :style="{ backgroundColor: color.hex }"
                ></div>
              </label>
            </div>
          </div>

          <!-- Size Selector -->
          <div v-if="sizesForSelectedColor.length" class="space-y-4">
            <div class="flex justify-between items-end">
              <span
                class="text-xs font-bold uppercase tracking-widest text-gray-400"
                >Select Size</span
              >
              <button
                class="text-xs font-medium underline text-gray-500 hover:text-primary"
              >
                Size Guide
              </button>
            </div>
            <div class="grid grid-cols-4 gap-2">
              <label
                v-for="variant in sizesForSelectedColor"
                :key="variant.id"
                class="cursor-pointer"
              >
                <input
                  type="radio"
                  name="size"
                  class="sr-only peer"
                  :value="variant.size"
                  v-model="selectedSize"
                  :disabled="variant.stock_quantity === 0"
                />
                <div
                  class="h-12 flex items-center justify-center border border-gray-200 dark:border-gray-700 rounded text-sm font-medium peer-checked:border-primary peer-checked:text-primary peer-checked:bg-primary/5 hover:bg-gray-50 dark:hover:bg-gray-800 transition-all uppercase"
                  :class="{
                    'opacity-30 cursor-not-allowed':
                      variant.stock_quantity === 0,
                  }"
                >
                  {{ variant.size }}
                </div>
              </label>
            </div>
          </div>

          <!-- CTA Buttons -->
          <div class="space-y-3 pt-4">
            <button
              @click="addToCart"
              class="w-full bg-primary hover:bg-primary/90 text-white h-14 rounded-lg font-bold text-base tracking-wide transition-all flex items-center justify-center gap-3"
            >
              <span class="material-symbols-outlined text-xl"
                >shopping_cart</span
              >
              Add to Bag
            </button>
            <button
              class="w-full bg-white dark:bg-transparent border border-[#dbdfe6] dark:border-gray-700 hover:border-gray-400 h-14 rounded-lg font-bold text-base tracking-wide transition-all"
            >
              Save to Wishlist
            </button>
          </div>

          <!-- Details Accordion -->
          <div
            class="divide-y divide-gray-100 dark:divide-gray-800 border-t border-gray-100 dark:border-gray-800"
          >
            <details class="group py-5" open>
              <summary
                class="flex justify-between items-center cursor-pointer list-none"
              >
                <span class="text-xs font-bold uppercase tracking-widest"
                  >Product Details</span
                >
                <span
                  class="material-symbols-outlined text-gray-400 group-open:rotate-180 transition-transform"
                  >expand_more</span
                >
              </summary>
              <div
                class="mt-4 text-sm text-gray-600 dark:text-gray-400 leading-relaxed space-y-2"
              >
                <p>• Premium Quality Materials</p>
                <p>• Modern athletic silhouette</p>
                <p>• Ethically sourced</p>
              </div>
            </details>
          </div>
        </div>
      </div>
    </div>
  </main>

  <div v-else class="max-w-[1440px] mx-auto px-6 lg:px-12 py-24 text-center">
    <h2 class="text-2xl font-bold">Product not found.</h2>
    <router-link to="/" class="text-primary hover:underline mt-4 inline-block"
      >Back to Home</router-link
    >
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { apiUrl } from "../api/client.js";

const route = useRoute();
const product = ref(null);
const variants = ref([]);
const productImages = ref([]);
const mainImage = ref("");
const loading = ref(true);

const selectedColor = ref("");
const selectedSize = ref("");

const fetchProduct = async () => {
  loading.value = true;
  try {
    const res = await fetch(
      apiUrl(`/api/products/${route.params.id}`),
    );
    const data = await res.json();
    product.value = data.product;
    variants.value = data.variants;
    productImages.value = data.images;
    mainImage.value = data.product.image_url;

    // Set initial selection
    if (data.variants.length) {
      selectedColor.value = data.variants[0].color_name;
      selectedSize.value = data.variants[0].size;
    }
  } catch (err) {
    console.error("Error fetching product:", err);
  } finally {
    loading.value = false;
  }
};

const setMainImage = (url) => {
  mainImage.value = url;
};

const uniqueColors = computed(() => {
  const colors = [];
  const seen = new Set();
  variants.value.forEach((v) => {
    if (!seen.has(v.color_name)) {
      seen.add(v.color_name);
      colors.push({ name: v.color_name, hex: v.color_hex });
    }
  });
  return colors;
});

const sizesForSelectedColor = computed(() => {
  return variants.value.filter((v) => v.color_name === selectedColor.value);
});

const addToCart = () => {
  alert(
    `Added ${product.value.name} (${selectedColor.value} / ${selectedSize.value}) to bag!`,
  );
};

onMounted(fetchProduct);
watch(() => route.params.id, fetchProduct);
</script>
