import {useFetch} from "#app";
const settings = {
    SERVER: true
}
import { UserData } from '~/store/user.ts';

export function getUserToken() {
  const user = UserData();
  return user.getToken();
}

export default () => {
    const config = useRuntimeConfig()
    return {
        get: (request, opt={}) => {
            if(!opt.hasOwnProperty('server')) {
                opt.server = true
            }
            return useFetch(request, {baseURL: config.public.baseURL, ...opt})
        },
        $get: (request, opt) => {
            // console.log('token is', getUserToken())
            return useFetch(request, {baseURL: config.public.baseURL, ...opt, server: settings.SERVER,
                onRequest({ request, options }) {
                    // Set the request headers
                    options.headers = options.headers || {}
                    options.headers.Authorization = `Token ${getUserToken()}`
                }
            })
        },
        post: (request, opt) => {
            return useFetch(request, {baseURL: config.public.baseURL, ...opt, server: settings.SERVER,
                method: 'POST'})
        },
        $post: (request, opt) => {
            return useFetch(request, {baseURL: config.public.baseURL, ...opt, server: settings.SERVER,
                method: 'POST',
                onRequest({ request, options }) {
                    // Set the request headers
                    options.headers = options.headers || {}
                    options.headers.Authorization = `Token ${getUserToken()}`
                }
            })
        },

    }
}