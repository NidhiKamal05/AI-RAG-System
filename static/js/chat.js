import { sendQuery } from "./api.js"
import { appendMessage, formatBotReply, showLoader, hideLoader } from "./ui.js"

const queryInput = document.getElementById("query_input") ;
const sendBtn = document.getElementById("send_btn") ;

sendBtn.addEventListener("click", async() => {
    const query = queryInput.value.trim() ;
    if(!query) return ;
    
    appendMessage("user", query) ;
    queryInput.value = "" ;
    
    showLoader() ;
    
    try {
        const result = await sendQuery(query) ;
        hideLoader() ;
        appendMessage("bot", formatBotReply(result)) ;
    }
    catch(error) {
        hideLoader() ;
        appendMessage( "bot", `<span class="text-danger"> Error: ${error.message} </span>` ) ;
    }
}) ;