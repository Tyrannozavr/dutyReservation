import {defineStore} from "pinia";

interface  UserState {
    first_name: string,
    last_name: string | null,
    username: string | null,
    language_code: string | null,
    origin: string | null,
}

export const useUserStore = defineStore('user', {
    state: (): UserState => {
        return {
            first_name: "",
            last_name: null,
            username: null,
            language_code: null,
            origin: null
        }

    },
    actions: {
        setOrigin (origin: string) {
            this.origin = origin
        }
    },
    getters: {
    },
      persist: true,
})