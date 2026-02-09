<template>
  <div class="home">
    <!-- Hero Section -->
    <section v-if="hero" class="relative h-[85vh] w-full overflow-hidden">
      <div
        class="absolute inset-0 bg-cover bg-center transition-opacity duration-1000"
        :style="{
          backgroundImage: `url(${hero.image_url})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }"
      >
        <div class="absolute inset-0 bg-black/10"></div>
      </div>
      <div
        class="relative h-full max-w-[1440px] mx-auto px-8 flex flex-col justify-center items-start"
      >
        <div class="max-w-xl space-y-6">
          <p
            class="text-white text-sm font-bold tracking-[0.3em] uppercase opacity-90"
          >
            SS24 Collection
          </p>
          <h2
            class="text-white text-7xl font-light leading-[1.1] tracking-tighter"
            v-html="hero.title"
          ></h2>
          <p class="text-white/90 text-lg font-light leading-relaxed max-w-md">
            {{ hero.subtitle }}
          </p>
          <div class="pt-4">
            <router-link
              :to="hero.button_link || '/search'"
              class="bg-white text-black px-10 py-4 rounded-full text-sm font-bold uppercase tracking-widest hover:bg-black hover:text-white transition-all duration-300 inline-block"
            >
              {{ hero.button_text }}
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- New Arrivals Section -->
    <section class="max-w-[1440px] mx-auto px-8 py-24">
      <div class="flex items-end justify-between mb-16">
        <div>
          <h3 class="text-3xl font-light tracking-tight mb-2">New Arrivals</h3>
          <p class="text-gray-500 dark:text-gray-400 font-light">
            Freshly curated pieces for your wardrobe
          </p>
        </div>
        <router-link
          to="/search"
          class="text-sm font-bold uppercase tracking-widest border-b-2 border-primary pb-1"
          >View All</router-link
        >
      </div>

      <div
        v-if="loading"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-12"
      >
        <div v-for="i in 4" :key="i" class="animate-pulse">
          <div class="aspect-[3/4] bg-gray-200 rounded-lg mb-4"></div>
          <div class="h-4 bg-gray-200 w-3/4 mb-2"></div>
          <div class="h-3 bg-gray-200 w-1/2"></div>
        </div>
      </div>

      <div
        v-else
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-x-8 gap-y-12"
      >
        <div
          v-for="product in newArrivals"
          :key="product.id"
          class="product-card group cursor-pointer"
          @click="goToProduct(product.id)"
        >
          <div
            class="relative aspect-[3/4] overflow-hidden bg-[#f6f6f8] rounded-lg mb-4"
          >
            <img
              :src="product.image_url"
              :alt="product.name"
              class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
              loading="lazy"
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
            <p class="text-gray-500 dark:text-gray-400 text-sm font-light">
              {{ product.description }}
            </p>
            <p class="text-primary font-medium mt-2">${{ product.price }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Newsletter Section -->
    <section class="bg-[#f0f2f4] dark:bg-gray-900 py-24 px-8">
      <div class="max-w-[800px] mx-auto text-center space-y-8">
        <div class="space-y-4">
          <h2 class="text-4xl font-light tracking-tight">Stay in the Loop</h2>
          <p
            class="text-gray-500 dark:text-gray-400 font-light max-w-md mx-auto"
          >
            Subscribe for early access to new collections and exclusive
            minimalist content.
          </p>
        </div>
        <form
          @submit.prevent="handleSubscribe"
          class="flex flex-col md:flex-row gap-4 items-center justify-center max-w-lg mx-auto"
        >
          <input
            v-model="email"
            class="w-full bg-white dark:bg-background-dark border-none rounded-lg h-14 px-6 focus:ring-2 focus:ring-primary/20 transition-all text-sm"
            placeholder="Email Address"
            type="email"
            required
          />
          <button
            type="submit"
            class="w-full md:w-auto min-w-[140px] bg-primary text-white h-14 px-8 rounded-lg font-bold text-sm uppercase tracking-widest hover:brightness-110 transition-all"
          >
            Subscribe
          </button>
        </form>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { apiUrl } from "../api/client.js";

const router = useRouter();
const hero = ref(null);
const newArrivals = ref([]);
const loading = ref(true);
const email = ref("");

const fetchHomeData = async () => {
  try {
    const [heroRes, productsRes] = await Promise.all([
      fetch(apiUrl("/api/hero-banners")),
      fetch(apiUrl("/api/products")),
    ]);

    const heroData = await heroRes.json();
    const productsData = await productsRes.json();

    hero.value = heroData[0];
    newArrivals.value = productsData
      .filter((p) => p.is_new_arrival)
      .slice(0, 4);
  } catch (err) {
    console.error("Error fetching home data:", err);
  } finally {
    loading.value = false;
  }
};

const goToProduct = (id) => {
  router.push({ name: "product-detail", params: { id } });
};

const handleSubscribe = () => {
  alert("Thank you for subscribing!");
  email.value = "";
};

onMounted(fetchHomeData);
</script>

<style scoped>
.product-card:hover .wishlist-btn {
  opacity: 1;
  transform: translateY(0);
}
</style>
