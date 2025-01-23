import type {FetchMethods, TokenResponse} from "~/types/auth";
import {useAuthStore} from "~/store/auth";
import {useUserStore} from "~/store/user";

export function refreshAccessToken(refreshUrl: string, refreshToken: string) {
    return useFetch<TokenResponse>(refreshUrl, {
        method: "post",
        body: JSON.stringify({
            refresh_token: refreshToken
        }),
        onResponse({response}) {
            if (response.status !== 200) {
                console.error("Refresh token: ", response)
            }
        }
    });
}

export async function fetchWithAuth(
    url: string, opt: object = {},
    baseURL: string, method: FetchMethods) {
    const authStore = useAuthStore()
    const accessToken = authStore.accessToken

    return useFetch(url, {
        baseURL: baseURL,
        method: method,
        ...opt,
        onRequest({options}) {
            options.headers.set("Authorization", `Bearer ${accessToken}`);
        }
    });
}


export async function fetchWithRefreshToken(
    url: string, opt: object = {},
    baseURL: string, method: FetchMethods, refreshURL: string) {
    const authStore = useAuthStore()
    const userStore = useUserStore()
    const refreshToken = authStore.refreshToken
    const performFetch = async (attempt: number = 1) => {
        const response = await fetchWithAuth(url, opt, baseURL, method)
        if (response.error.value?.statusCode === 401 && attempt === 1) {
            refreshURL = `${baseURL}${refreshURL}`
            const {data: tokens} = await refreshAccessToken(refreshURL, refreshToken)
            if (tokens.value) {
                authStore.setTokens(tokens.value.access_token, tokens.value.refresh_token)
                return await performFetch(attempt += 1)
            } else {
                if (userStore.origin === "telegram") {
                    navigateTo("/auth/telegram")
                } else {
                    navigateTo("/auth")
                }
            }
        }
        return response
    }
    return performFetch()
}











