// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2024-11-01',
    devtools: {enabled: true},
    runtimeConfig: {
        public: {
            baseURL: process.env.NUXT_API_URL,
            telegramInitData: process.env.NUXT_TELEGRAM_INIT_DATA,
        },
    },
    app: {
        head: {
            script: [{src: 'https://telegram.org/js/telegram-web-app.js'}],
        },
    },
    modules: [
        '@pinia/nuxt',
        'pinia-plugin-persistedstate/nuxt',
        '@nuxt/ui',
    ],
    vite: {
        server: {
            allowedHosts: ['6b43-219-100-37-233.ngrok-free.app'],
        },
    },
})