let hasShownWelcomeInSession = false;

function toggleChat() {
  const chatbox = document.getElementById("chatbox");
  const messages = document.getElementById("messages");

  if (chatbox.style.display === "block" || chatbox.style.display === "flex") {
    chatbox.style.display = "none";
    chatbox.classList.remove("maximized");
  } else {
    chatbox.style.display = "flex";

    // Sadece session'da ilk açılışta welcome mesajı göster
    if (!hasShownWelcomeInSession) {
      showBotMessage("Merhaba, ben Piri Reis Üniversitesinin Yapay Zeka Asistanı **PiriX**! Size nasıl yardımcı olabilirim? ⚓", false);
      hasShownWelcomeInSession = true;
    }
  }
}

function makeLinksOpenInNewTab(html) {
  return html.replace(/<a\s+/g, '<a target="_blank" rel="noopener noreferrer" ');
}

let controller = null;
let isBotResponding = false;

function sendMessage() {
  if (isBotResponding) return;

  const input = document.getElementById("user-input");
  const sendBtn = document.getElementById("send-button");
  const stopBtn = document.getElementById("stop-button");
  const messages = document.getElementById("messages");
  
  const msg = input.value.trim();
  if (!msg) return;

  // Gönder butonunu kilitle, durdur butonunu göster
  if (sendBtn) {
    sendBtn.disabled = true;
    sendBtn.classList.add("blocked");
  }
  if (stopBtn) stopBtn.style.display = "inline-block";

  isBotResponding = true;

  // Önceki isteği iptal et
  if (controller) controller.abort();
  controller = new AbortController();

  // Kullanıcı mesajını ekle
  const userMessageDiv = document.createElement("div");
  userMessageDiv.className = "chat-message user";
  userMessageDiv.innerHTML = msg;
  messages.appendChild(userMessageDiv);
  input.value = "";
  
  // Yeni yazıyor göstergesini ekle
  showTypingIndicator();
  messages.scrollTop = messages.scrollHeight;

  fetch("http://127.0.0.1:8000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: msg, session_id: sessionId}),
    signal: controller.signal,
  })
    .then((res) => res.json())
    .then((data) => {
      const rawMarkdown = data.answer;
      const feedbackId = data.feedback_id;
      let html = marked.parse(rawMarkdown);
      html = makeLinksOpenInNewTab(html);

      // Yazma göstergesini kaldır
      const typingDiv = document.getElementById('typing');
      if (typingDiv) {
        // Yeni yanıt mesajı oluştur
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message", "bot");
        messageDiv.innerHTML = html;
        messageDiv.setAttribute("data-feedback-id", feedbackId);
        
        // Feedback butonları ekle
        addFeedbackButtons(messageDiv);
        
        // Yazma göstergesini yeni mesajla değiştir
        messages.replaceChild(messageDiv, typingDiv);
      }
      
      resetButtons();
    })
    .catch((err) => {
      // Yazma göstergesini kaldır
      const typingDiv = document.getElementById('typing');
      if (typingDiv) {
        if (err.name === "AbortError") {
          typingDiv.innerHTML = "<i>Yanıt durduruldu.</i>";
        } else {
          typingDiv.innerHTML = "Bir hata oluştu. Lütfen tekrar deneyin.";
          console.error("Hata:", err);
        }
      }
      resetButtons();
    });
}

function stopResponse() {
  if (controller) controller.abort();
  resetButtons();
}

function resetButtons() {
  const sendBtn = document.getElementById("send-button");
  const stopBtn = document.getElementById("stop-button");

  if (sendBtn) {
    sendBtn.disabled = false;
    sendBtn.classList.remove("blocked");
  }
  if (stopBtn) stopBtn.style.display = "none";

  isBotResponding = false;
}

function showBotMessage(markdownText, showFeedback = false) {
  const messages = document.getElementById("messages");

  const messageDiv = document.createElement("div");
  messageDiv.classList.add("chat-message", "bot");

  let html = marked.parse(markdownText);
  html = makeLinksOpenInNewTab(html);
  messageDiv.innerHTML = html;

  if (showFeedback) {
    addFeedbackButtons(messageDiv);
  }

  messages.appendChild(messageDiv);
  messages.scrollTop = messages.scrollHeight;
}

// YENİ YAZMA ANİMASYON FONKSİYONU
function showTypingIndicator() {
  const messages = document.getElementById("messages");
  
  // Yeni yazıyor balonu oluştur
  const yazıyorDiv = document.createElement('div');
  yazıyorDiv.className = 'yazıyor-balonu';
  yazıyorDiv.id = 'typing';
  
  // Logo alanı oluştur
  const logoDiv = document.createElement('div');
  logoDiv.className = 'yazıyor-logo';
  
  // Logo olarak P harfini ekle (sabit ve kesin çalışacak çözüm)
  const logoText = document.createElement('span');
  logoText.textContent = 'P';
  logoText.style.color = 'white';
  logoText.style.fontWeight = 'bold';
  logoText.style.fontSize = '14px';
  logoDiv.appendChild(logoText);
  
  // Yazıyor metni oluştur
  const textDiv = document.createElement('div');
  textDiv.className = 'yazıyor-text';
  textDiv.textContent = 'Yazıyor';
  
  // Noktalar için alan oluştur
  const noktalarDiv = document.createElement('div');
  noktalarDiv.className = 'yazıyor-noktalar';
  
  // 3 nokta ekle
  for (let i = 0; i < 3; i++) {
    const nokta = document.createElement('span');
    nokta.className = 'yazıyor-nokta';
    noktalarDiv.appendChild(nokta);
  }
  
  // Hepsini birleştir
  textDiv.appendChild(noktalarDiv);
  yazıyorDiv.appendChild(logoDiv);
  yazıyorDiv.appendChild(textDiv);
  
  messages.appendChild(yazıyorDiv);
  messages.scrollTop = messages.scrollHeight;
}

document.addEventListener("DOMContentLoaded", function () {
  const userInput = document.getElementById("user-input");
  if (userInput) {
    userInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !isBotResponding) {
        sendMessage();
      }
    });
  }
});

const bubble = document.querySelector(".chat-bubble");

window.addEventListener("load", () => {
  const chatbox = document.getElementById("chatbox");
  if (chatbox) {
    chatbox.style.display = "none";
  }
  if (bubble) {
    bubble.classList.add("show-bubble");
    setTimeout(() => {
      bubble.classList.remove("show-bubble");
    }, 6000);
  }
});

setInterval(() => {
  if (bubble) {
    bubble.classList.add("show-bubble");
    setTimeout(() => {
      bubble.classList.remove("show-bubble");
    }, 6000);
  }
}, 12000);

const toggleButton = document.querySelector(".chatbot-toggle");
toggleButton.addEventListener("mouseenter", () => {
  if (bubble) {
    bubble.classList.add("show-bubble");
    setTimeout(() => {
      bubble.classList.remove("show-bubble");
    }, 6000);
  }
});

window.addEventListener("click", function (e) {
  const chatbox = document.getElementById("chatbox");
  const toggleBtn = document.querySelector(".chatbot-toggle");
  if (
    chatbox.style.display === "flex" &&
    !chatbox.contains(e.target) &&
    !toggleBtn.contains(e.target)
  ) {
    chatbox.style.display = "none";
    chatbox.classList.remove("maximized");
  }
});

function closeChatbox() {
  const chatbox = document.getElementById("chatbox");
  chatbox.style.display = "none";
  chatbox.classList.remove("maximized");
}

function toggleMaximize() {
  const chatbox = document.getElementById("chatbox");
  const icon = document.getElementById("maximize-icon");

  chatbox.classList.toggle("maximized");

  if (chatbox.classList.contains("maximized")) {
    icon.textContent = "❐";
  } else {
    icon.textContent = "🗖";
  }
}

let isDragging = false;
let startY = 0;

const resizeHandle = document.getElementById("resize-handle");

if (resizeHandle) {
  resizeHandle.addEventListener("mousedown", (e) => {
    isDragging = true;
    startY = e.clientY;
  });

  window.addEventListener("mousemove", (e) => {
    if (isDragging) {
      const deltaY = startY - e.clientY;
      if (deltaY > 50) {
        chatbox.classList.add("expanded");
        isDragging = false;
      }
    }
  });

  window.addEventListener("mouseup", () => {
    isDragging = false;
  });
}

function addFeedbackButtons(elem) {
  const feedback = document.createElement("div");
  feedback.classList.add("feedback");

  const likeBtn = document.createElement("button");
  likeBtn.classList.add("feedback-btn", "like-btn");
  likeBtn.setAttribute("aria-label", "Beğendim");
  likeBtn.setAttribute("data-tooltip", "Yanıtı beğendim");
  likeBtn.innerHTML = '<i class="fa-regular fa-thumbs-up"></i>';

  const dislikeBtn = document.createElement("button");
  dislikeBtn.classList.add("feedback-btn", "dislike-btn");
  dislikeBtn.setAttribute("aria-label", "Beğenmedim");
  dislikeBtn.setAttribute("data-tooltip", "Yanıtı beğenmedim");
  dislikeBtn.innerHTML = '<i class="fa-regular fa-thumbs-down"></i>';

  const feedbackId = elem.getAttribute("data-feedback-id");

  likeBtn.addEventListener("click", () => {
    if (likeBtn.disabled) return;

    likeBtn.disabled = true;
    likeBtn.classList.add("active");

    dislikeBtn.disabled = false;
    dislikeBtn.classList.remove("active");

    if (feedbackId) {
      sendFeedback(feedbackId, "like");
    }

    showThankYouToast();
  });

  dislikeBtn.addEventListener("click", () => {
    if (dislikeBtn.disabled) return;

    dislikeBtn.disabled = true;
    dislikeBtn.classList.add("active");

    likeBtn.disabled = false;
    likeBtn.classList.remove("active");

    if (feedbackId) {
      sendFeedback(feedbackId, "dislike");
    }

    showThankYouToast();
  });

  feedback.append(likeBtn, dislikeBtn);
  elem.appendChild(feedback);
}

function sendFeedback(feedbackId, feedbackType) {
  fetch("http://127.0.0.1:8000/feedback", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      feedback_id: feedbackId,
      feedback_type: feedbackType,
      session_id: sessionId
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      console.log("Feedback gönderildi:", data);
    })
    .catch((err) => {
      console.error("Feedback gönderme hatası:", err);
    });
}

function showThankYouToast() {
  const toast = document.getElementById("feedback-toast");
  if (!toast) return;

  toast.style.display = "block";
  toast.style.opacity = "1";
  toast.style.pointerEvents = "auto";

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.pointerEvents = "none";
    setTimeout(() => {
      toast.style.display = "none";
    }, 300);
  }, 3000);
}