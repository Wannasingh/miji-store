import { ref } from "vue";

const toasts = ref([]);
let nextId = 1;
let defaultDuration = 4000;

/**
 * แสดง popup เตือนผู้ใช้
 * @param {string} message - ข้อความ
 * @param {'success'|'warning'|'error'|'info'} type
 * @param {number} duration - ms (0 = ไม่ปิดเอง)
 */
export function useToast() {
  function show(message, type = "info", duration = defaultDuration) {
    const id = nextId++;
    const toast = { id, message, type };
    toasts.value.push(toast);
    if (duration > 0) {
      setTimeout(() => {
        remove(id);
      }, duration);
    }
    return id;
  }

  function remove(id) {
    toasts.value = toasts.value.filter((t) => t.id !== id);
  }

  return { toasts, show, remove };
}
