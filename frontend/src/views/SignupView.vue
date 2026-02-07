<template>
  <div class="min-h-[80vh] flex items-center justify-center px-6 py-12">
    <div
      class="max-w-md w-full space-y-8 bg-white dark:bg-gray-900 p-10 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-800"
    >
      <div class="text-center">
        <h2 class="text-3xl font-black tracking-tight uppercase">Join Miji</h2>
        <p class="mt-2 text-sm text-gray-500 font-light">
          Create an account for a better experience
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleSignup">
        <div class="space-y-4">
          <div>
            <label
              for="name"
              class="block text-xs font-bold uppercase tracking-widest text-gray-400 mb-2"
              >Full Name</label
            >
            <input
              id="name"
              v-model="name"
              type="text"
              required
              class="appearance-none relative block w-full px-4 py-3 border border-gray-200 dark:border-gray-700 placeholder-gray-400 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all sm:text-sm dark:bg-background-dark dark:text-white"
              placeholder="John Doe"
            />
          </div>
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
              placeholder="Minimum 8 characters"
            />
          </div>
        </div>

        <div class="flex items-center">
          <input
            id="terms"
            name="terms"
            type="checkbox"
            required
            class="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
          />
          <label
            for="terms"
            class="ml-2 block text-sm text-gray-500 font-light"
          >
            I agree to the
            <a href="#" class="font-medium text-primary hover:underline"
              >Terms of Service</a
            >
          </label>
        </div>

        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-4 px-4 border border-transparent text-sm font-bold rounded-lg text-white bg-primary hover:brightness-110 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all uppercase tracking-widest"
          >
            Create Account
          </button>
        </div>

        <div class="text-center mt-6">
          <p class="text-sm text-gray-500 font-light">
            Already have an account?
            <router-link
              to="/login"
              class="font-bold text-primary hover:underline"
              >Sign in</router-link
            >
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const name = ref("");
const email = ref("");
const password = ref("");

const handleSignup = () => {
  // Mock signup
  console.log("Signup attempt:", name.value, email.value);
  alert("Account created successfully (Mock)");
  router.push("/login");
};
</script>
