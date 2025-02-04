import {defineStore} from "pinia";

interface  UserState {
    user_id: number | null,
    first_name: string,
    last_name: string | null,
    username: string | null,
    language_code: string | null,
    origin: string | null,
    photo_url: string | null
}

export const useUserStore = defineStore('user', {
    state: (): UserState => {
        return {
            user_id: null,
            first_name: "",
            last_name: null,
            username: null,
            language_code: null,
            origin: null,
            photo_url: null
        }

    },
    actions: {
        setOrigin (origin: string) {
            this.origin = origin
        },
        clearData () {
            this.first_name = ""
            this.last_name = ""
            this.username = ""
            this.language_code = ""
            this.origin = ""
            this.photo_url = ""
            this.user_id = null
        }
    },
    getters: {
    },
      persist: true,
})