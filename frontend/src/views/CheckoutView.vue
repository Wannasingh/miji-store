<template>
  <main class="max-w-[1440px] mx-auto px-6 lg:px-12 py-12">
    <div class="max-w-4xl mx-auto">
      <!-- Steps Indicator -->
      <nav class="flex items-center justify-between mb-16 relative">
        <div
          class="absolute top-1/2 left-0 w-full h-0.5 bg-gray-100 -translate-y-1/2 -z-10"
        ></div>
        <div
          class="absolute top-1/2 left-0 h-0.5 bg-primary -translate-y-1/2 -z-10 transition-all duration-500"
          :style="{ width: `${(currentStep - 1) * 50}%` }"
        ></div>

        <div
          v-for="step in 3"
          :key="step"
          class="flex flex-col items-center gap-3"
        >
          <div
            class="size-10 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-300"
            :class="
              currentStep >= step
                ? 'bg-primary text-white scale-110 shadow-lg'
                : 'bg-white border-2 border-gray-200 text-gray-400'
            "
          >
            {{ step }}
          </div>
          <span
            class="text-[10px] uppercase font-bold tracking-widest"
            :class="currentStep >= step ? 'text-primary' : 'text-gray-400'"
          >
            {{ stepNames[step - 1] }}
          </span>
        </div>
      </nav>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-12">
        <!-- Main Form Area -->
        <div class="lg:col-span-2">
          <transition name="fade" mode="out-in">
            <!-- Step 1: Shipping -->
            <div v-if="currentStep === 1" class="space-y-8">
              <h2 class="text-2xl font-black uppercase tracking-tight">
                Shipping Information
              </h2>
              <div class="grid grid-cols-2 gap-4">
                <div class="col-span-1 space-y-2">
                  <label
                    class="text-[10px] uppercase font-bold text-gray-400 tracking-widest"
                    >First Name</label
                  >
                  <input
                    v-model="form.firstName"
                    type="text"
                    class="w-full bg-[#f0f2f4] border-none rounded-lg p-3 text-sm focus:ring-1 focus:ring-primary/20"
                  />
                </div>
                <div class="col-span-1 space-y-2">
                  <label
                    class="text-[10px] uppercase font-bold text-gray-400 tracking-widest"
                    >Last Name</label
                  >
                  <input
                    v-model="form.lastName"
                    type="text"
                    class="w-full bg-[#f0f2f4] border-none rounded-lg p-3 text-sm focus:ring-1 focus:ring-primary/20"
                  />
                </div>
                <div class="col-span-2 space-y-2">
                  <label
                    class="text-[10px] uppercase font-bold text-gray-400 tracking-widest"
                    >Address</label
                  >
                  <input
                    v-model="form.address"
                    type="text"
                    class="w-full bg-[#f0f2f4] border-none rounded-lg p-3 text-sm focus:ring-1 focus:ring-primary/20"
                  />
                </div>
              </div>
              <button
                @click="currentStep = 2"
                class="w-full bg-primary text-white py-4 rounded-lg font-bold uppercase tracking-widest text-sm hover:brightness-110"
              >
                Continue to Payment
              </button>
            </div>

            <!-- Step 2: Payment -->
            <div v-else-if="currentStep === 2" class="space-y-8">
              <h2 class="text-2xl font-black uppercase tracking-tight">
                Payment Details
              </h2>
              <div class="space-y-4">
                <div
                  class="p-4 border-2 border-primary bg-primary/5 rounded-lg flex items-center justify-between"
                >
                  <div class="flex items-center gap-3">
                    <span class="material-symbols-outlined text-primary"
                      >credit_card</span
                    >
                    <span class="text-sm font-bold">Credit / Debit Card</span>
                  </div>
                  <div
                    class="size-4 rounded-full border-4 border-primary"
                  ></div>
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div class="col-span-2 space-y-2">
                    <label
                      class="text-[10px] uppercase font-bold text-gray-400 tracking-widest"
                      >Card Number</label
                    >
                    <input
                      type="text"
                      placeholder="**** **** **** ****"
                      class="w-full bg-[#f0f2f4] border-none rounded-lg p-3 text-sm focus:ring-1 focus:ring-primary/20"
                    />
                  </div>
                </div>
              </div>
              <div class="flex gap-4">
                <button
                  @click="currentStep = 1"
                  class="flex-1 border border-gray-200 py-4 rounded-lg font-bold uppercase tracking-widest text-sm hover:bg-gray-50"
                >
                  Back
                </button>
                <button
                  @click="currentStep = 3"
                  class="flex-1 bg-primary text-white py-4 rounded-lg font-bold uppercase tracking-widest text-sm hover:brightness-110"
                >
                  Review Order
                </button>
              </div>
            </div>

            <!-- Step 3: Review -->
            <div v-else-if="currentStep === 3" class="space-y-8">
              <h2 class="text-2xl font-black uppercase tracking-tight">
                Review Order
              </h2>
              <div class="bg-gray-50 rounded-xl p-6 space-y-6">
                <div class="flex justify-between items-start">
                  <div>
                    <h4
                      class="text-[10px] uppercase font-bold text-gray-400 tracking-widest mb-2"
                    >
                      Shipping to
                    </h4>
                    <p class="text-sm">
                      {{ form.firstName }} {{ form.lastName }}
                    </p>
                    <p class="text-sm text-gray-500">{{ form.address }}</p>
                  </div>
                  <button
                    @click="currentStep = 1"
                    class="text-primary text-[10px] font-bold uppercase tracking-widest"
                  >
                    Edit
                  </button>
                </div>
              </div>
              <button
                @click="placeOrder"
                class="w-full bg-primary text-white py-4 rounded-lg font-bold uppercase tracking-widest text-sm hover:brightness-110"
              >
                Place Order - $214.00
              </button>
            </div>
          </transition>
        </div>

        <!-- Sidebar Summary -->
        <div class="lg:col-span-1">
          <div
            class="bg-white border border-gray-100 rounded-2xl p-6 space-y-6 shadow-sm"
          >
            <h3 class="text-sm font-bold uppercase tracking-widest">
              Order Summary
            </h3>
            <div class="space-y-4">
              <div class="flex gap-4">
                <div
                  class="size-16 bg-gray-100 rounded-lg overflow-hidden shrink-0"
                >
                  <img
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuC4FGw39OWITriYqfHjEfLGU0d-bfZRsha7Lf73IIv9FVvGyW1h7u5N-OiGdgvhfCEt64fnlhIh6tyTiknXed2uWP9kH77h3fcjOvspCi15GSMnSJwTrehmkUdZbtWOcWXXefkkdXoZxeWVSB67OO1lDtgOV1aQSWQFkMqRFFNJccQAPwBfDrsqSlXCi2UOOXoKSzIdf1Xed3XFzOBlEZdnUDpCVEOj-NUBZUrozVuRy1LS_6_4fPtL1lFG0ZSYYI154tsKYUqt7pmX"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div class="flex-1 min-w-0">
                  <h4
                    class="text-xs font-bold truncate uppercase tracking-tight"
                  >
                    Premium Merino Polo
                  </h4>
                  <p class="text-[10px] text-gray-400 uppercase">
                    Size: S / Qty: 1
                  </p>
                  <p class="text-xs font-black mt-1">$125.00</p>
                </div>
              </div>
              <div class="flex gap-4">
                <div
                  class="size-16 bg-gray-100 rounded-lg overflow-hidden shrink-0"
                >
                  <img
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuAszW4nmU022Z4Stef_k4Th3beRbjxvl8v9TKoFgERI2gflOMvjNxa1yruD5XJ6AfRGM-9qib004MfCkuIKUelZ1x7DPNAM7gGhMWxcEEdUstvJnlBuguJQ-h6o9iW3tufntW-RPzEO0nKRvq2J1Sa6HK-qosAKctFV0I6AzTn920Op7lKpM0mV-v33gR3ogQat4ZYW2Gj7_zrxD0nvc9XYv-yZUrdR_F9bXVAyDRSun_9tUqeEhAHvSKwGBHOLKNtGEWsDPfOt3M2U"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div class="flex-1 min-w-0">
                  <h4
                    class="text-xs font-bold truncate uppercase tracking-tight"
                  >
                    Linen Trousers
                  </h4>
                  <p class="text-[10px] text-gray-400 uppercase">
                    Size: M / Qty: 1
                  </p>
                  <p class="text-xs font-black mt-1">$89.00</p>
                </div>
              </div>
            </div>

            <div class="border-t border-gray-100 pt-6 space-y-2">
              <div class="flex justify-between text-sm text-gray-500">
                <span>Subtotal</span>
                <span>$214.00</span>
              </div>
              <div class="flex justify-between text-sm text-gray-500">
                <span>Shipping</span>
                <span
                  class="text-green-600 font-bold uppercase tracking-widest text-[10px]"
                  >Free</span
                >
              </div>
              <div class="flex justify-between text-base font-black pt-4">
                <span>Total</span>
                <span>$214.00</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const currentStep = ref(1);
const stepNames = ["Shipping", "Payment", "Review"];

const form = reactive({
  firstName: "",
  lastName: "",
  address: "",
  email: "",
});

const placeOrder = () => {
  alert("Order placed successfully!");
  router.push("/");
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>
