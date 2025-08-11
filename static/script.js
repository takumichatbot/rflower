// script.js
document.addEventListener('DOMContentLoaded', () => {
    // 質問例ボタンがクリックされたときの処理
    document.querySelectorAll('.example-btn').forEach(button => {
        button.addEventListener('click', () => {
            const question = button.textContent;
            sendMessage(question);
        });
    });
});

async function sendMessage(message = null) {
    const userInput = document.getElementById('user-input');
    const userMessage = message || userInput.value.trim();

    if (userMessage === '') return;

    // ユーザーメッセージをチャット画面に追加
    addMessageToChat('user', userMessage);
    userInput.value = '';

    // ローディングメッセージを表示（一意のクラス名とIDを追加）
    const loadingMessageId = 'loading-' + new Date().getTime();
    addMessageToChat('bot', '...', true, loadingMessageId);

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        });

        if (!response.ok) {
            throw new Error(`サーバーエラー: ${response.status}`);
        }

        const data = await response.json();
        
        // ローディングメッセージを削除
        removeLoadingMessage(loadingMessageId);

        // AIの回答をチャット画面に追加
        addMessageToChat('bot', data.answer);

    } catch (error) {
        console.error('Fetchエラー:', error);
        
        // ローディングメッセージを削除
        removeLoadingMessage(loadingMessageId);

        // タイムアウトやネットワークエラーの場合のメッセージ
        addMessageToChat('bot', '申し訳ありませんが、ネットワーク接続に問題が発生しました。しばらくしてから再度お試しください。');
    }
}

function addMessageToChat(sender, message, isLoading = false, id = null) {
    const messagesContainer = document.getElementById('chatbot-messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);

    if (isLoading) {
        messageDiv.classList.add('loading-message');
        if (id) {
            messageDiv.id = id;
        }
    }

    // URLをリンクに変換する処理
    const linkifiedMessage = message.replace(
        /(https?:\/\/[^\s<>"'()]+)/g,
        '<a href="$1" target="_blank">$1</a>'
    );
    
    // HTMLとして挿入
    messageDiv.innerHTML = linkifiedMessage; 

    messagesContainer.appendChild(messageDiv);
    // 自動スクロール
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeLoadingMessage(id) {
    const loadingMessageElement = document.getElementById(id);
    if (loadingMessageElement) {
        loadingMessageElement.remove();
    }
}


function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}