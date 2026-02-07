<template>
  <main class="max-w-[1440px] mx-auto px-6 lg:px-12 py-24">
    <div class="max-w-4xl mx-auto space-y-16">
      <div class="text-center space-y-4">
        <h1 class="text-5xl font-black uppercase tracking-tighter">
          Help & FAQ
        </h1>
        <p class="text-gray-500 font-light">
          Find answers to common questions about our products and services.
        </p>
      </div>

      <div class="space-y-4">
        <details
          v-for="i in 5"
          :key="i"
          class="group bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-sm"
        >
          <summary
            class="flex justify-between items-center p-6 cursor-pointer list-none font-bold uppercase tracking-tight text-sm"
          >
            <span>Frequently Asked Question #{{ i }}</span>
            <span
              class="material-symbols-outlined text-gray-400 group-open:rotate-180 transition-transform"
              >expand_more</span
            >
          </summary>
          <div class="px-6 pb-6 text-sm text-gray-500 leading-relaxed">
            Our minimalist pieces are crafted with the highest attention to
            detail. We use ethically sourced materials and sustainable practices
            to ensure quality over quantity. Shipping takes 3-5 business days
            worldwide.
          </div>
        </details>
      </div>

      <div class="bg-primary/5 rounded-3xl p-12 text-center space-y-6">
        <h3 class="text-2xl font-black uppercase tracking-tight">
          Still have questions?
        </h3>
        <p class="text-gray-500">
          Our team is available 24/7 to assist you with your order.
        </p>
        <router-link
          to="/contact"
          class="inline-block bg-primary text-white px-10 py-4 rounded-full font-bold uppercase tracking-widest text-sm hover:brightness-110"
          >Contact Support</router-link
        >
      </div>
    </div>
  </main>
</template>
