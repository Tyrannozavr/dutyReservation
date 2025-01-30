import {fetchWithRefreshToken} from "~/services/clientApi";
import type {options} from "~/composables/api"

export const useClientFetch = () => {
    const config = useRuntimeConfig();

    return {
        get: async <T>(url: string, opt: options = {}) => {
                return $fetch<T>(url, {
                    baseURL: config.public.baseURL,
                    method: "GET",
                    ...opt,
                })

        },
        $get: async <T>(url: string, opt: object = {}) => {
            return fetchWithRefreshToken(
                url, opt, config.public.baseURL, "GET", "/auth/token/refresh",
            )
        },
        post: async <T>(url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return $fetch<T>(url, {
                baseURL: config.public.baseURL,
                method: "POST",
                ...opt,
            })
        },
        $post: async <T>(url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return fetchWithRefreshToken<T>(
                url, opt, config.public.baseURL, "POST", "/auth/token/refresh",
            )
        },
        delete: async <T>(url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return $fetch<T>(url, {
                baseURL: config.public.baseURL,
                method: "DELETE",
                ...opt,
            })
        },
        $delete: async <T>(url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return fetchWithRefreshToken<T>(
                url, opt, config.public.baseURL, "DELETE", "/auth/token/refresh",
            )
        },

        put: async <T>(url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return $fetch<T>(url, {
                baseURL: config.public.baseURL,
                method: "PUT",
                ...opt,
            })
        },
        $put: async <T>(url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return fetchWithRefreshToken<T>(
                url, opt, config.public.baseURL, "PUT", "/auth/token/refresh",
            )
        },
        patch: async <T>(url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return $fetch<T>(url, {
                baseURL: config.public.baseURL,
                method: "PATCH",
                ...opt,
            })
        },
        $patch: async <T>(url: string, opt: options = {}) => {
            if (opt.hasOwnProperty('body') && opt.body !== null && typeof opt.body === "object") {
                opt.body = JSON.stringify(opt.body)
            }
            return fetchWithRefreshToken<T>(
                url, opt, config.public.baseURL, "PATCH", "/auth/token/refresh",
            )
        },
    };
}
