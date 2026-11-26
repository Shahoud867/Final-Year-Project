/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_STATIC_EXPORT?: string;
}
interface ImportMeta {
  readonly env: ImportMetaEnv;
}
