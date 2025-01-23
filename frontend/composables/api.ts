import {useAuthStore} from "~/store/auth";
import type {FetchMethods, TokenResponse} from "~/types/auth";
import {useUserStore} from "~/store/user";
import {fetchWithRefreshToken} from "~/services/api";




export const useBackend = () => {
    const config = useRuntimeConfig();
    const authStore = useAuthStore();
    const userStore = useUserStore();

    return {
        $post: async (url: string, opt: object = {}) => {
            return fetchWithRefreshToken(
                url, opt, config.public.baseURL, "POST", "/auth/token/refresh",
            )
        },
        $get: async (url: string, opt: object = {}) => {
            // Create a function to perform the fetch request
            const performFetch = async (attempt = 1) => {
                // Use useFetch to make the request
                const response = await useFetch(url, {
                    baseURL: config.public.baseURL,
                    method: "get",
                    ...opt,
                    onRequest({ options }) {
                        options.headers.set("Authorization", `Bearer ${authStore.accessToken}`);
                    }
                });

                // if (response.error.value?.statusCode === 401 && attempt === 1) {
                //     // Attempt to refresh the token
                //     const { data: tokens, error: refreshError } = await refreshToken(
                //         `${config.public.baseURL}/auth/token/refresh`,
                //         authStore.refreshToken
                // );
                //
                //     if (tokens.value) {
                //         console.log("There is a tokens value", tokens.value)
                //         // Set new tokens in auth store
                //         authStore.setTokens(tokens.value.access_token, tokens.value.refresh_token);
                //         // Retry the original request with the new access token
                //         return await performFetch(attempt + 1); // Increment attempt count
                //     } else {
                //         // Handle redirection based on user origin
                //         if (userStore.origin === "telegram") {
                //             navigateTo("/auth/telegram");
                //         } else {
                //             navigateTo("/auth");
                //         }
                //     }
                // }

                return response
            };
            return await performFetch(); // Call the fetch function
        }
    };
}