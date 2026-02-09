<template>
  <div class="min-h-[80vh] flex items-center justify-center px-6 py-12">
    <div
      class="max-w-md w-full space-y-8 bg-white dark:bg-gray-900 p-10 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800"
    >
      <div class="text-center">
        <h2 class="text-3xl font-black tracking-tight uppercase">
          Welcome Back
        </h2>
        <p class="mt-2 text-sm text-gray-500 font-light">
          Enter your details to access your account
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="space-y-4">
          <div>
            <label
              for="email"
              class="block text-xs font-bold uppercase tracking-widest text-gray-400 mb-2"
              >Email Address</label
            >
            <input
              id="email"
              v-model="email"
              type="email"
              required
              class="appearance-none relative block w-full px-4 py-3 border border-gray-200 dark:border-gray-700 placeholder-gray-400 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all sm:text-sm dark:bg-background-dark dark:text-white"
              placeholder="name@example.com"
            />
          </div>
          <div>
            <label
              for="password"
              class="block text-xs font-bold uppercase tracking-widest text-gray-400 mb-2"
              >Password</label
            >
            <input
              id="password"
              v-model="password"
              type="password"
              required
              class="appearance-none relative block w-full px-4 py-3 border border-gray-200 dark:border-gray-700 placeholder-gray-400 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all sm:text-sm dark:bg-background-dark dark:text-white"
              placeholder="••••••••"
            />
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
            />
            <label
              for="remember-me"
              class="ml-2 block text-sm text-gray-500 font-light"
              >Remember me</label
            >
          </div>
          <div class="text-sm">
            <a href="#" class="font-medium text-primary hover:underline"
              >Forgot password?</a
            >
          </div>
        </div>

        <div>
          <button
            type="submit"
            :disabled="loading"
            class="group relative w-full flex justify-center py-4 px-4 border border-transparent text-sm font-bold rounded-lg text-white bg-primary hover:brightness-110 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all uppercase tracking-widest disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {{ loading ? "กำลังเข้าสู่ระบบ..." : "Sign in" }}
          </button>
        </div>

        <div class="text-center mt-6">
          <p class="text-sm text-gray-500 font-light">
            Don't have an account?
            <router-link
              to="/signup"
              class="font-bold text-primary hover:underline"
              >Create one</router-link
            >
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { setToken } from "../utils/auth.js";
import { useToast } from "../composables/useToast.js";
import { apiUrl } from "../api/client.js";

const router = useRouter();
const route = useRoute();
const toast = useToast();
const email = ref("");
const password = ref("");
const loading = ref(false);

async function handleLogin() {
  loading.value = true;
  try {
    const res = await fetch(apiUrl("/api/auth/login"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.value, password: password.value }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      toast.show(data.error || "ล็อกอินไม่สำเร็จ", "error");
      return;
    }
    setToken(data.token);
    toast.show("ล็อกอินสำเร็จ", "success");
    router.push(route.query.redirect || "/");
  } catch (e) {
    toast.show("เกิดข้อผิดพลาด กรุณาลองใหม่", "error");
  } finally {
    loading.value = false;
  }
}
</script>
