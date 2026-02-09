import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import { isAuthenticated } from "../utils/auth.js";
import { useToast } from "../composables/useToast.js";

const TITLE_SUFFIX = "| Miji Store";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: { title: "MINIMALIST " + TITLE_SUFFIX },
    },
    {
      path: "/login",
      name: "login",
      component: LoginView,
      meta: { title: "Login " + TITLE_SUFFIX },
    },
    {
      path: "/signup",
      name: "signup",
      component: SignupView,
      meta: { title: "Sign Up " + TITLE_SUFFIX },
    },
    {
      path: "/product/:id",
      name: "product-detail",
      component: () => import("../views/ProductDetailView.vue"),
      meta: { title: "Product " + TITLE_SUFFIX },
    },
    {
      path: "/search",
      name: "search",
      component: () => import("../views/SearchView.vue"),
      meta: { title: "Shop " + TITLE_SUFFIX },
    },
    {
      path: "/checkout",
      name: "checkout",
      component: () => import("../views/CheckoutView.vue"),
      meta: { title: "Checkout " + TITLE_SUFFIX, requiresAuth: true },
    },
    {
      path: "/contact",
      name: "contact",
      component: () => import("../views/ContactView.vue"),
      meta: { title: "Contact " + TITLE_SUFFIX },
    },
    {
      path: "/help",
      name: "help",
      component: () => import("../views/HelpView.vue"),
      meta: { title: "Help " + TITLE_SUFFIX },
    },
    {
      path: "/wishlist",
      name: "wishlist",
      component: () => import("../views/WishlistView.vue"),
      meta: { title: "Wishlist " + TITLE_SUFFIX, requiresAuth: true },
    },
    {
      path: "/:pathMatch(.*)*",
      name: "not-found",
      component: () => import("../views/NotFoundView.vue"),
      meta: { title: "404 Not Found " + TITLE_SUFFIX },
    },
  ],
  scrollBehavior() {
    return { top: 0 };
  },
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title || "MINIMALIST " + TITLE_SUFFIX;

  if (to.meta.requiresAuth && !isAuthenticated()) {
    useToast().show("กรุณาล็อกอินก่อนเข้าหน้านี้", "warning");
    next({ name: "login", query: { redirect: to.fullPath } });
    return;
  }
  next();
});

export default router;
