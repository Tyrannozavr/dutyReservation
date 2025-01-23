import {fetchWithRefreshToken} from "~/services/api";




export const useBackend = () => {
    const config = useRuntimeConfig();

    return {
        $post: async (url: string, opt: object = {}) => {
            return fetchWithRefreshToken(
                url, opt, config.public.baseURL, "POST", "/auth/token/refresh",
            )
        },
        $get: async (url: string, opt: object = {}) => {
            return fetchWithRefreshToken(
                url, opt, config.public.baseURL, "GET", "/auth/token/refresh",
            )
        },
    };
}