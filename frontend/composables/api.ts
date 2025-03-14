import {fetchWithRefreshToken} from "~/services/api";

export type options = {
    body?: object | null | string,
}

export const useBackend = () => {
    const config = useRuntimeConfig();

    return {
        get: async <T>(url: string, opt: options = {}) => {
            return useFetch<T>(url, {
                baseURL: config.public.baseURL,
                method: "GET",
                ...opt,
            })
        },
        $get: async <T>(url: string, opt: object = {}) => {
            return fetchWithRefreshToken<T>(
                url, opt, config.public.baseURL, "GET", "/auth/token/refresh",
            )
        },
        post: async (url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return useFetch(url, {
                baseURL: config.public.baseURL,
                method: "POST",
                ...opt,
            })
        },
        $post: async (url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return fetchWithRefreshToken(
                url, opt, config.public.baseURL, "POST", "/auth/token/refresh",
            )
        },
        patch: async (url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return useFetch(url, {
                baseURL: config.public.baseURL,
                method: "PATCH",
                ...opt,
            })
        },
        $patch: async (url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return fetchWithRefreshToken(
                url, opt, config.public.baseURL, "PATCH", "/auth/token/refresh",
            )
        },
        delete: async (url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return useFetch(url, {
                baseURL: config.public.baseURL,
                method: "DELETE",
                ...opt,
            })
        },
        $delete: async (url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return fetchWithRefreshToken(
                url, opt, config.public.baseURL, "DELETE", "/auth/token/refresh",
            )
        },
    };
}
