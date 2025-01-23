import {fetchWithRefreshToken} from "~/services/api";

export const useBackend = () => {
    const config = useRuntimeConfig();

    return {
        get: async (url: string, opt: object = {}) => {
            return useFetch(url, {
                baseURL: config.public.baseURL,
                method: "GET",
                ...opt,
            })
        },
        $get: async (url: string, opt: object = {}) => {
            return fetchWithRefreshToken(
                url, opt, config.public.baseURL, "GET", "/auth/token/refresh",
            )
        },
        post: async (url: string, opt: object = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return useFetch(url, {
                baseURL: config.public.baseURL,
                method: "POST",
                ...opt,
            })
        },
        $post: async (url: string, opt: object = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return fetchWithRefreshToken(
                url, opt, config.public.baseURL, "POST", "/auth/token/refresh",
            )
        },

    };
}