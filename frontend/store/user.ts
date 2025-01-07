import {defineStore} from "pinia";

interface  UserState {
    telegram_id: number | null,
    first_name: string,
    last_name: string | null,
    username: string | null,
    is_authenticated: boolean,
    token: string,
    language_code: string | null,
    set_telegram_data: (
        telegram_id: number,
        first_name: string,
        last_name?: string | null,
        username?: string | null,
        language_code?: string | null
    ) => void,
    getUserFio: () => string,
    getToken: () => string,
}

export const UserData = defineStore('user', {
    state: (): UserState => {
        return {
            telegram_id: null,
            first_name: "",
            last_name: null,
            username: null,
            is_authenticated: false,
            token: "",
            language_code: null
        }

    },
    actions: {
        getToken() {
            return this.token
        },
        getUserFio() {
            return `${this.first_name} ${this.last_name ? this.last_name : ""}`
        },
        setToken(token: string) {
            this.token = token
        },
        setAuthenticated(is_authenticated: boolean) {
            this.is_authenticated = is_authenticated
        },
        set_telegram_data(telegram_id: number, first_name: string, last_name: string | null = null,
                          username: string | null = null, language_code: string | null = null) {
            this.telegram_id = telegram_id
            this.first_name = first_name
            this.last_name = last_name
            this.username = username
            this.language_code = language_code
        }
    },
      persist: true,
})