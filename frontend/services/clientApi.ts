import type { FetchMethods, TokenResponse } from "~/types/auth";
import { useAuthStore } from "~/store/auth";
import { useUserStore } from "~/store/user";
import { navigateTo } from 'nuxt/app'; // Ensure you import navigateTo

export async function refreshAccessToken(refreshUrl: string, refreshToken: string) {
    try {
        const response = await $fetch<TokenResponse>(refreshUrl, {
            method: "POST",
            body: {
                refresh_token: refreshToken
            }
        });
        return response;
    } catch (error) {
        console.error("Refresh token error: ", error);
        throw error; // Rethrow the error for further handling
    }
}

export async function fetchWithAuth<T>(
    url: string,
    opt: object = {},
    baseURL: string,
    method: FetchMethods
) {
    const authStore = useAuthStore();
    const accessToken = authStore.accessToken;

    return await $fetch<T>(url, {
        baseURL,
        method,
        ...opt,
        headers: {
            Authorization: `Bearer ${accessToken}`,
            ...opt.headers // Spread existing headers if any
        }
    });
}

export async function fetchWithRefreshToken<T>(
    url: string,
    opt: object = {},
    baseURL: string,
    method: FetchMethods,
    refreshURL: string
) {
    const authStore = useAuthStore();
    const userStore = useUserStore();
    const refreshToken = authStore.refreshToken;

    const performFetch = async (attempt: number = 1) => {
        try {
            const response = await fetchWithAuth<T>(url, opt, baseURL, method);
            if (response.error?.statusCode === 401 && attempt === 1) {
                const fullRefreshUrl = `${baseURL}${refreshURL}`;
                const tokens = await refreshAccessToken(fullRefreshUrl, refreshToken);

                if (tokens) {
                    authStore.setTokens(tokens.access_token, tokens.refresh_token);
                    return await performFetch(attempt + 1);
                } else {
                    redirectUser(userStore.origin);
                }
            }
            return response;
        } catch (error) {
            console.error("Fetch error:", error);
            throw error; // Handle or rethrow as needed
        }
    };

    return await performFetch();
}

function redirectUser(origin: string) {
    if (origin === "telegram") {
        navigateTo("/auth/telegram");
    } else {
        navigateTo("/auth");
    }
}
