export const useAuthStore = defineStore('auth', {
    state: () => ({
        accessToken: 'testAccessToken',
        refreshToken: '',
        isAuthenticated: false,
        username: '',
    }),
    persist: true,
    actions: {
        setTokens(accessToken: string, refreshToken: string) {
            this.accessToken = accessToken;
            this.refreshToken = refreshToken;
        },
        clearTokens() {
            this.accessToken = '';
            this.refreshToken = '';
        },
        login(accessToken: string, refreshToken: string, username?: string): void {
            this.setTokens(accessToken, refreshToken);
            this.username = username ? username : ''
            this.isAuthenticated = true
        }
    },
})
