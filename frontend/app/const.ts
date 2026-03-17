export const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
export const MAX_FILE_SIZE_MB =
  Number(import.meta.env.VITE_MAX_FILE_SIZE_MB) || 25;
export const MAX_FILES = Number(import.meta.env.VITE_MAX_FILES) || 5;
