// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    compatibilityDate: '2024-11-01',
    devtools: {enabled: true},
    runtimeConfig: {
        public: {
            baseURL: process.env.NUXT_API_URL,
            frontURL: `https://${process.env.NUXT_API_HOST}`,
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
            allowedHosts: true,
            // allowedHosts: [process.env.NUXT_API_HOST],

        },
    },
})