export interface TokenResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
}

export type FetchMethods = "GET" | "POST" | "DELETE" | "get" | "HEAD" | "PATCH" | "PUT" | "CONNECT" | "OPTIONS" | "TRACE" | "post"
