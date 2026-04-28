import { API_URL } from "./config.js" ;

export async function sendQuery(query) {
    const chat_url= `${API_URL}/chat`
    const response = await fetch(chat_url, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ query }),
    }) ;
    return response.json() ;
}