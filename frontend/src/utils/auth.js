/**
 * Auth helper สำหรับ protect route — ใช้ localStorage เก็บ token
 * ต่อเมื่อต่อ backend จริงให้เปลี่ยนเป็นเรียก API + httpOnly cookie/JWT
 */
const AUTH_KEY = "miji_token";

export function getToken() {
  return localStorage.getItem(AUTH_KEY);
}

export function setToken(token) {
  localStorage.setItem(AUTH_KEY, token || "ok");
}

export function clearToken() {
  localStorage.removeItem(AUTH_KEY);
}

export function isAuthenticated() {
  return !!getToken();
}
