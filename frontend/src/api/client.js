/**
 * Base URL สำหรับเรียก Backend API
 * Development: ใช้ .env มี VITE_API_URL=http://localhost:8080
 * Production: ตั้ง VITE_API_URL เป็น URL ของ backend จริง (เช่น https://api.yourdomain.com)
 */
export const API_BASE = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");

export function apiUrl(path) {
  const p = path.startsWith("/") ? path : `/${path}`;
  return API_BASE ? `${API_BASE}${p}` : p;
}
