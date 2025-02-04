import {useUserStore} from "~/store/user";
import type {UserResponse} from "~/types/auth";


export async function fetchUserData() {
    const userStore = useUserStore()
    const $backend = useBackend()
    const { data: userData} = await $backend.$get<UserResponse>("/auth/me")
    if (userData.value) {
        userStore.first_name = userData.value.first_name
        userStore.last_name = userData.value.last_name
        userStore.username = userData.value.username
        userStore.photo_url = userData.value.photo_url
        userStore.user_id = userData.value.id
    }
}