<template>
  <main
    class="max-w-[1440px] mx-auto px-6 lg:px-12 py-24 text-center space-y-8"
  >
    <div class="space-y-4">
      <span class="material-symbols-outlined text-6xl text-gray-200"
        >favorite</span
      >
      <h1 class="text-4xl font-black uppercase tracking-tighter">
        Your Wishlist
      </h1>
      <p class="text-gray-500 font-light max-w-sm mx-auto">
        Keep track of the pieces you love. Start adding items from our
        collection.
      </p>
    </div>
    <router-link
      to="/search"
      class="inline-block bg-black text-white px-10 py-4 rounded-full font-bold uppercase tracking-widest text-sm hover:opacity-80"
      >Start Shopping</router-link
    >
  </main>
</template>
