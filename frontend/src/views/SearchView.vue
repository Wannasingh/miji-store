<template>
  <main class="max-w-[1440px] mx-auto px-6 lg:px-12 py-12">
    <div class="flex flex-col lg:flex-row gap-12">
      <!-- Sidebar Filters -->
      <aside class="w-full lg:w-64 space-y-10">
        <div>
          <h4 class="text-xs font-bold uppercase tracking-widest mb-6">
            Categories
          </h4>
          <ul class="space-y-4">
            <li>
              <button
                @click="selectedCategory = null"
                class="text-sm transition-colors"
                :class="
                  selectedCategory === null
                    ? 'font-bold text-primary border-b-2 border-primary'
                    : 'text-gray-500 hover:text-primary'
                "
              >
                All Items
              </button>
            </li>
            <li v-for="cat in categories" :key="cat.id">
              <button
                @click="selectedCategory = cat.id"
                class="text-sm transition-colors"
                :class="
                  selectedCategory === cat.id
                    ? 'font-bold text-primary border-b-2 border-primary'
                    : 'text-gray-500 hover:text-primary'
                "
              >
                {{ cat.name }}
              </button>
            </li>
          </ul>
        </div>

        <div>
          <h4 class="text-xs font-bold uppercase tracking-widest mb-6">
            Price Range
          </h4>
          <div class="space-y-4">
            <input
              type="range"
              v-model="maxPrice"
              min="0"
              max="500"
              class="w-full h-1 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary"
            />
            <div class="flex justify-between text-xs font-medium text-gray-500">
              <span>$0</span>
              <span>Up to ${{ maxPrice }}</span>
            </div>
          </div>
        </div>
      </aside>

      <!-- Product Grid -->
      <div class="flex-1">
        <div class="flex justify-between items-center mb-10">
          <h2 class="text-2xl font-black uppercase tracking-tight">
            {{ currentCategoryName }}
            <span class="text-gray-400 font-normal lowercase ml-2"
              >({{ filteredProducts.length }} items)</span
            >
          </h2>

          <div
            class="flex items-center gap-4 text-xs font-bold uppercase tracking-widest"
          >
            <span class="text-gray-400">Sort by:</span>
            <select
              v-model="sortBy"
              class="bg-transparent border-none focus:ring-0 p-0 text-gray-900 cursor-pointer"
            >
              <option value="newest">Newest</option>
              <option value="price-low">Price: Low to High</option>
              <option value="price-high">Price: High to Low</option>
            </select>
          </div>
        </div>

        <div
          v-if="loading"
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12"
        >
          <div v-for="i in 6" :key="i" class="animate-pulse">
            <div class="aspect-[3/4] bg-gray-100 rounded-lg mb-4"></div>
            <div class="h-4 bg-gray-100 w-3/4 mb-2"></div>
            <div class="h-3 bg-gray-100 w-1/2"></div>
          </div>
        </div>

        <div
          v-else-if="filteredProducts.length === 0"
          class="py-24 text-center space-y-4"
        >
          <span class="material-symbols-outlined text-6xl text-gray-200"
            >search_off</span
          >
          <h3 class="text-xl font-medium">No results found.</h3>
          <p class="text-gray-400">
            Try adjusting your filters or search query.
          </p>
          <button
            @click="resetFilters"
            class="text-primary hover:underline font-bold uppercase tracking-widest text-xs"
          >
            Clear All Filters
          </button>
        </div>

        <div
          v-else
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12"
        >
          <div
            v-for="product in filteredProducts"
            :key="product.id"
            class="product-card group cursor-pointer"
            @click="goToProduct(product.id)"
          >
            <div
              class="relative aspect-[3/4] overflow-hidden bg-[#f6f6f8] rounded-lg mb-4"
            >
              <img
                :src="product.image_url"
                class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
              />
              <button
                class="wishlist-btn opacity-0 translate-y-2 absolute top-4 right-4 bg-white/90 p-2 rounded-full shadow-sm hover:text-primary transition-all duration-300"
              >
                <span class="material-symbols-outlined text-xl">favorite</span>
              </button>
            </div>
            <div class="space-y-1">
              <h4
                class="text-sm font-medium text-gray-900 dark:text-gray-100 uppercase tracking-wide"
              >
                {{ product.name }}
              </h4>
              <p
                class="text-gray-500 dark:text-gray-400 text-sm font-light uppercase"
              >
                {{ product.categories?.name }}
              </p>
              <p class="text-primary font-medium mt-2">${{ product.price }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

const products = ref([]);
const categories = ref([]);
const loading = ref(true);

const selectedCategory = ref(null);
const maxPrice = ref(500);
const sortBy = ref("newest");
const searchQuery = ref(route.query.q || "");

const fetchData = async () => {
  loading.value = true;
  try {
    const [prodRes, catRes] = await Promise.all([
      fetch("http://127.0.0.1:5050/api/products"),
      fetch("http://127.0.0.1:5050/api/categories"),
    ]);
    products.value = await prodRes.json();
    categories.value = await catRes.json();
  } catch (err) {
    console.error("Error fetching data:", err);
  } finally {
    loading.value = false;
  }
};

const currentCategoryName = computed(() => {
  if (!selectedCategory.value) return "All Collections";
  const cat = categories.value.find((c) => c.id === selectedCategory.value);
  return cat ? cat.name : "Collections";
});

const filteredProducts = computed(() => {
  let result = [...products.value];

  // Filter by Category
  if (selectedCategory.value) {
    result = result.filter((p) => p.category_id === selectedCategory.value);
  }

  // Filter by Search Query
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    result = result.filter(
      (p) =>
        p.name.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q),
    );
  }

  // Filter by Price
  result = result.filter((p) => p.price <= maxPrice.value);

  // Sort
  if (sortBy.value === "price-low") {
    result.sort((a, b) => a.price - b.price);
  } else if (sortBy.value === "price-high") {
    result.sort((a, b) => b.price - a.price);
  }

  return result;
});

const resetFilters = () => {
  selectedCategory.value = null;
  maxPrice.value = 500;
  searchQuery.value = "";
  router.replace({ query: {} });
};

const goToProduct = (id) => {
  router.push({ name: "product-detail", params: { id } });
};

onMounted(fetchData);

watch(
  () => route.query.q,
  (newQ) => {
    searchQuery.value = newQ || "";
  },
);
</script>

<style scoped>
.product-card:hover .wishlist-btn {
  opacity: 1;
  transform: translateY(0);
}
</style>
