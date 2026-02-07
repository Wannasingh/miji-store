<template>
  <main class="max-w-[1440px] mx-auto px-6 lg:px-12 py-24">
    <div class="max-w-2xl mx-auto space-y-12">
      <div class="text-center space-y-4">
        <h1 class="text-5xl font-black uppercase tracking-tighter">
          Contact Us
        </h1>
        <p class="text-gray-500 font-light">
          We're here to help you with anything you need.
        </p>
      </div>

      <form
        class="space-y-6 bg-white border border-gray-100 p-10 rounded-3xl shadow-sm"
      >
        <div class="grid grid-cols-2 gap-6">
          <div class="space-y-2">
            <label
              class="text-[10px] uppercase font-bold text-gray-400 tracking-widest"
              >Name</label
            >
            <input
              type="text"
              class="w-full bg-[#f0f2f4] border-none rounded-lg p-3 text-sm focus:ring-1 focus:ring-primary/20"
              placeholder="Your name"
            />
          </div>
          <div class="space-y-2">
            <label
              class="text-[10px] uppercase font-bold text-gray-400 tracking-widest"
              >Email</label
            >
            <input
              type="email"
              class="w-full bg-[#f0f2f4] border-none rounded-lg p-3 text-sm focus:ring-1 focus:ring-primary/20"
              placeholder="email@example.com"
            />
          </div>
        </div>
        <div class="space-y-2">
          <label
            class="text-[10px] uppercase font-bold text-gray-400 tracking-widest"
            >Message</label
          >
          <textarea
            rows="5"
            class="w-full bg-[#f0f2f4] border-none rounded-lg p-3 text-sm focus:ring-1 focus:ring-primary/20"
            placeholder="How can we help?"
          ></textarea>
        </div>
        <button
          type="submit"
          class="w-full bg-primary text-white py-4 rounded-lg font-bold uppercase tracking-widest text-sm hover:brightness-110"
        >
          Send Message
        </button>
      </form>

      <div
        class="grid grid-cols-3 gap-8 text-center pt-12 border-t border-gray-100"
      >
        <div class="space-y-2">
          <span class="material-symbols-outlined text-primary">mail</span>
          <p class="text-xs font-bold uppercase tracking-widest">Email</p>
          <p class="text-sm text-gray-500">hello@minimalist.com</p>
        </div>
        <div class="space-y-2">
          <span class="material-symbols-outlined text-primary">call</span>
          <p class="text-xs font-bold uppercase tracking-widest">Phone</p>
          <p class="text-sm text-gray-500">+1 (555) 000-0000</p>
        </div>
        <div class="space-y-2">
          <span class="material-symbols-outlined text-primary"
            >location_on</span
          >
          <p class="text-xs font-bold uppercase tracking-widest">Studio</p>
          <p class="text-sm text-gray-500">Bangkok, Thailand</p>
        </div>
      </div>
    </div>
  </main>
</template>
