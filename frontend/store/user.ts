import {defineStore} from "pinia";

interface  UserState {
    first_name: string,
    last_name: string | null,
    username: string | null,
    is_authenticated: boolean,
    access_token: string | null,
    refresh_token: string | null,
    language_code: string | null,
    set_telegram_data: (
        first_name: string,
        last_name?: string | null,
        username?: string | null,
        language_code?: string | null
    ) => void,
    getAccessToken: () => string,
    getRefreshToken: () => string,
    getUserFio: () => string,
    setToken: (token: string) => void,
    authenticateUser: (access_token: string, refresh_token: string) => void
}

export const UserData = defineStore('user', {
    state: (): UserState => {
        return {
            first_name: "",
            last_name: null,
            username: null,
            is_authenticated: false,
            access_token: null,
            refresh_token: null,
            language_code: null
        }

    },
    actions: {
        getAccessToken() {
            return this.access_token
        },
        getRefreshToken() {
            return this.refresh_token
        },
        getUserFio() {
            return `${this.first_name} ${this.last_name ? this.last_name : ""}`
        },
        setTelegramData(first_name: string, last_name: string | null = null,
                          username: string | null = null, language_code: string | null = null) {
            this.first_name = first_name
            this.last_name = last_name
            this.username = username
            this.language_code = language_code
        },
        authenticateUser(access_token: string, refresh_token: string) {
            this.access_token = access_token
            this.refresh_token = refresh_token
            this.is_authenticated = true
        }
    },
      persist: true,
})