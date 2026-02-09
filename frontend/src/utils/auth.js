import { ref } from "vue";

/**
 * Auth helper สำหรับ protect route — ใช้ localStorage เก็บ token
 * ต่อเมื่อต่อ backend จริงให้เปลี่ยนเป็นเรียก API + httpOnly cookie/JWT
 */
const AUTH_KEY = "miji_token";

/** Reactive state เพื่อให้ Navbar อัปเดตทันทีเมื่อ login/logout */
export const authState = ref(!!localStorage.getItem(AUTH_KEY));

function syncAuthState() {
  authState.value = !!localStorage.getItem(AUTH_KEY);
}

export function getToken() {
  return localStorage.getItem(AUTH_KEY);
}

export function setToken(token) {
  localStorage.setItem(AUTH_KEY, token || "ok");
  authState.value = true;
}

export function clearToken() {
  localStorage.removeItem(AUTH_KEY);
  authState.value = false;
}

export function isAuthenticated() {
  return !!getToken();
}

/** ใช้ใน Navbar เพื่อให้เช็ค state จาก localStorage (เช่น เปิดแท็บใหม่) */
export function refreshAuthState() {
  syncAuthState();
}
