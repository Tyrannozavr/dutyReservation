import { useFetch } from "#app";
import { UserData } from '~/store/user.ts';

const settings = {
    SERVER: false
}

export function getUserToken() {
    const user = UserData();
    return user.getAccessToken();
}

export function getRefreshToken() {
    const user = UserData();
    return user.getRefreshToken(); // Ensure you have a method to get the refresh token
}

async function refreshAccessToken() {
    const refreshToken = getRefreshToken();
    const response = await fetch(`${useRuntimeConfig().public.baseURL}/auth/token/refresh`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ refresh_token: refreshToken })
    });

    if (response.ok) {
        const data = await response.json();
        // Update tokens in your store or local storage
        UserData().setToken(data.access_token);
        UserData().setRefreshToken(data.refresh_token); // Ensure you have a method to set the refresh token
        return data.access_token; // Return the new access token
    } else {
        console.error("Failed to refresh token", await response.json());
        // Handle redirection to login or other logic
        window.location.href = '/auth'; // Adjust as necessary for your app
        throw new Error('Failed to refresh token');
    }
}

export default () => {
    const config = useRuntimeConfig();

    return {
        get: (request, opt = {}) => {
            if (!opt.hasOwnProperty('server')) {
                opt.server = true;
            }
            return useFetch(request, { baseURL: config.public.baseURL, ...opt });
        },

        $get: async (request, opt) => {
            try {
                return await useFetch(request, {
                    baseURL: config.public.baseURL,
                    ...opt,
                    server: settings.SERVER,
                    onRequest({ options }) {
                        options.headers = options.headers || {};
                        options.headers.Authorization = `Token ${getUserToken()}`;
                    }
                });
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    const newToken = await refreshAccessToken(); // Try refreshing the token
                    return useFetch(request, {
                        baseURL: config.public.baseURL,
                        ...opt,
                        server: settings.SERVER,
                        onRequest({ options }) {
                            options.headers = options.headers || {};
                            options.headers.Authorization = `Token ${newToken}`; // Use the new token
                        }
                    });
                }
                throw error; // Rethrow if not a 401 error
            }
        },

        post: (request, opt) => {
            console.log("post is")
            return useFetch(request, { baseURL: config.public.baseURL, ...opt, server: settings.SERVER, method: 'POST' });
        },

        $post: async (request, opt) => {
            try {
                return await useFetch(request, {
                    baseURL: config.public.baseURL,
                    ...opt,
                    server: settings.SERVER,
                    method: 'POST',
                    onRequest({ options }) {
                        options.headers = options.headers || {};
                        options.headers.Authorization = `Token ${getUserToken()}`;
                    }
                });
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    const newToken = await refreshAccessToken(); // Try refreshing the token
                    return useFetch(request, {
                        baseURL: config.public.baseURL,
                        ...opt,
                        server: settings.SERVER,
                        method: 'POST',
                        onRequest({ options }) {
                            options.headers = options.headers || {};
                            options.headers.Authorization = `Token ${newToken}`; // Use the new token
                        }
                    });
                }
                throw error; // Rethrow if not a 401 error
            }
        },
    }
}
