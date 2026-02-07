<template>
  <footer
    class="bg-white dark:bg-background-dark border-t border-[#f0f2f4] dark:border-gray-800 pt-20 pb-10 px-8"
  >
    <div class="max-w-[1440px] mx-auto">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-20">
        <div class="space-y-6">
          <div class="flex items-center gap-2">
            <div class="text-primary size-5">
              <svg
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
            <h2 class="text-lg font-bold tracking-tight">MINIMALIST</h2>
          </div>
          <p
            class="text-gray-500 dark:text-gray-400 text-sm font-light leading-relaxed"
          >
            Curating timeless pieces that define the modern aesthetic. Quality
            over quantity, always.
          </p>
        </div>
        <div>
          <h5 class="text-sm font-bold uppercase tracking-widest mb-6">
            Collections
          </h5>
          <ul
            class="space-y-4 text-sm font-light text-gray-500 dark:text-gray-400"
          >
            <li>
              <router-link
                class="hover:text-primary transition-colors"
                to="/search?category=Womens-dresses"
                >Women's Essentials</router-link
              >
            </li>
            <li>
              <router-link
                class="hover:text-primary transition-colors"
                to="/search?category=Mens-shirts"
                >Men's Basics</router-link
              >
            </li>
            <li>
              <router-link
                class="hover:text-primary transition-colors"
                to="/search?category=Womens-bags"
                >Accessories</router-link
              >
            </li>
            <li>
              <router-link
                class="hover:text-primary transition-colors"
                to="/search"
                >Summer 24</router-link
              >
            </li>
          </ul>
        </div>
        <div>
          <h5 class="text-sm font-bold uppercase tracking-widest mb-6">
            Support
          </h5>
          <ul
            class="space-y-4 text-sm font-light text-gray-500 dark:text-gray-400"
          >
            <li>
              <router-link
                class="hover:text-primary transition-colors"
                to="/help"
                >Shipping Policy</router-link
              >
            </li>
            <li>
              <router-link
                class="hover:text-primary transition-colors"
                to="/help"
                >Returns & Exchanges</router-link
              >
            </li>
            <li>
              <router-link
                class="hover:text-primary transition-colors"
                to="/contact"
                >Contact Us</router-link
              >
            </li>
            <li>
              <router-link
                class="hover:text-primary transition-colors"
                to="/help"
                >FAQ</router-link
              >
            </li>
          </ul>
        </div>
        <div>
          <h5 class="text-sm font-bold uppercase tracking-widest mb-6">
            Social
          </h5>
          <div class="flex gap-4">
            <a
              href="#"
              class="size-10 rounded-full border border-gray-200 dark:border-gray-700 flex items-center justify-center text-gray-600 dark:text-gray-300 hover:border-primary hover:text-primary transition-all"
            >
              <i class="fab fa-instagram"></i>
            </a>
            <a
              href="#"
              class="size-10 rounded-full border border-gray-200 dark:border-gray-700 flex items-center justify-center text-gray-600 dark:text-gray-300 hover:border-primary hover:text-primary transition-all"
            >
              <i class="fab fa-twitter"></i>
            </a>
          </div>
        </div>
      </div>
      <div
        class="border-t border-[#f0f2f4] dark:border-gray-800 pt-10 flex flex-col md:flex-row justify-between items-center gap-6"
      >
        <p class="text-xs text-gray-400 font-light">
          © 2024 MINIMALIST. All rights reserved.
        </p>
        <div
          class="flex gap-8 text-[10px] text-gray-400 uppercase tracking-widest font-bold"
        >
          <router-link class="hover:text-primary transition-colors" to="/help"
            >Privacy</router-link
          >
          <router-link class="hover:text-primary transition-colors" to="/help"
            >Terms</router-link
          >
          <router-link class="hover:text-primary transition-colors" to="/help"
            >Cookies</router-link
          >
        </div>
      </div>
    </div>
  </footer>
</template>
