const chatBox = document.getElementById("chat_box") ;

export function appendMessage(role, text) {
    const msg = document.createElement("div") ;
    msg.className = role === "user" ? "text-end text-primary mb-2": "text-start text-dark mb-2" ;
    msg.innerHTML = `<strong>${role}:</strong>${text}` ;
    chatBox.appendChild(msg) ;
    chatBox.scrollTop = chatBox.scrollHeight ; ;
}

export function showLoader() {
	  const loader = document.createElement("div") ;
	  loader.id = "loader" ;
	  loader.className = "loaader mb-2" ;
	  loader.textContent = "Thinking..." ;
	  chatBox.appendChild(loader) ;
	  chatBox.scrollTop = chatBox.scrollHeight ; ;
}

export function hideLoader() {
    const loader = document.getElementById("loader") ;
    if(loader) {
      loader.remove() ;
    }
}

export function formatBotReply(result) {
    return `
        ${result.answer}<br>
        <small class="text-muted">
          Confidence: ${result.confidence} | Source: ${result.source}(chunk #${result.chunk_id}) | Latency: ${result.latency}s
        </small>
    `;
}