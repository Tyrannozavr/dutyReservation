import {useAuthStore} from "~/store/auth";
import type {TokenResponse} from "~/types/auth";

async function refreshToken(refreshUrl: string, refreshToken: string) {
    return useFetch<TokenResponse>(refreshUrl, {
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


export const useBackend = () => {
    const config = useRuntimeConfig()
    const authStore = useAuthStore()
    return {
        $get: async (url: string, opt: object = {}) => {
            return useFetch(
                url,
                {
                    baseURL: config.public.baseURL,
                    method: "get",
                    ...opt,
                    onRequest({request, options}) {
                        options.headers.set("Authorization", `Bearer ${authStore.accessToken}`)
                    },
                    onResponse({response}) {
                        if (response.status === 401) {
                            // console.log("need to refresh token")
                            let tokens = refreshToken(
                                `${config.public.baseURL}/auth/token/refresh`,
                                authStore.refreshToken
                            )
                            console.log("refreshed tokens are", tokens)
                        }
                    }
                }
            )
        }


    }
}