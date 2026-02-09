<template>
  <div
    class="min-h-[80vh] flex flex-col items-center justify-center px-6 py-16 text-center"
  >
    <p class="text-8xl font-black text-gray-200 dark:text-gray-800 tracking-tighter">
      404
    </p>
    <h1 class="mt-4 text-2xl font-bold tracking-tight uppercase text-primary dark:text-white">
      Page Not Found
    </h1>
    <p class="mt-2 max-w-sm text-sm text-gray-500 font-light">
      The page you're looking for doesn't exist or has been moved.
    </p>
    <router-link
      to="/"
      class="mt-8 inline-flex items-center justify-center px-6 py-3 border border-transparent text-sm font-bold rounded-lg text-white bg-primary hover:brightness-110 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all uppercase tracking-widest"
    >
      Back to Home
    </router-link>
  </div>
</template>

<script setup>
// 404 — title set via route meta in router
</script>
