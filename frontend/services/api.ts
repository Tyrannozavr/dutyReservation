import type {FetchMethods, TokenResponse} from "~/types/auth";
import {useAuthStore} from "~/store/auth";

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
    url: string, accessToken: string, opt: object = {},
    baseURL: string, method: FetchMethods) {
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
    const refreshToken = authStore.refreshToken
    const accessToken = authStore.accessToken
    const performFetch = async (attempt: number = 1) => {
        const response = await fetchWithAuth(url, accessToken, opt, baseURL, method)
        if (response.error.value?.statusCode === 401 && attempt === 1) {
            refreshURL = `${baseURL}${refreshURL}`
            const { data: tokens } = await refreshAccessToken(refreshURL, refreshToken)
            if (tokens.value) {
                console.log("Tokens value")
                authStore.setTokens(tokens.value.access_token, tokens.value.refresh_token)
            }
        }
        return response
    }
    return performFetch()
}











