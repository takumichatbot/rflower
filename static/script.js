// static/script.js
function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();

    if (message === '') {
        return; // 入力が空の場合は何もしない
    }

    appendMessage(message, 'user-message');
    userInput.value = ''; // 入力フィールドをクリア

    // チャットボットAPIにメッセージを送信
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        appendMessage(data.answer, 'bot-message');
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage('エラーが発生しました。もう一度お試しください。', 'bot-message');
    });
}

function appendMessage(text, className) {
    const messagesDiv = document.getElementById('chatbot-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', className);
    messageElement.textContent = text;
    messagesDiv.appendChild(messageElement);
    // 最新のメッセージが見えるようにスクロール
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
