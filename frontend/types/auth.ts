export interface TokenResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
}
export interface UserResponse {
    username: string
    first_name: string
    last_name: string | null
    link: string | null
}
export type FetchMethods = "GET" | "POST" | "DELETE" | "get" | "HEAD" | "PATCH" | "PUT" | "CONNECT" | "OPTIONS" | "TRACE" | "post"
