<template>
  <main
    class="max-w-[1440px] mx-auto px-6 lg:px-12 py-24 text-center space-y-8"
  >
    <div class="space-y-4">
      <span
        class="material-symbols-outlined text-6xl text-gray-200 dark:text-gray-600"
        >person</span
      >
      <h1 class="text-4xl font-black uppercase tracking-tighter">
        โปรไฟล์
      </h1>
      <p class="text-gray-500 dark:text-gray-400 font-light max-w-sm mx-auto">
        จัดการบัญชีและข้อมูลของคุณ
      </p>
    </div>
    <router-link
      to="/search"
      class="inline-block bg-primary text-white dark:bg-primary dark:text-white px-10 py-4 rounded-full font-bold uppercase tracking-widest text-sm hover:opacity-90 transition-opacity"
      >ไปช้อปปิ้ง</router-link
    >
  </main>
</template>

<script setup>
// หน้านี้ต้อง login จึงเข้าได้ (meta.requiresAuth)
</script>
