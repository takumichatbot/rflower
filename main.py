# main.py
from flask import Flask, render_template, request, jsonify
from qa_data import qa_pairs
from flask_cors import CORS # CORSを追加

app = Flask(__name__)
CORS(app) # 全てのオリジンからのアクセスを許可（開発用。本番環境では制限を推奨）

def get_answer(question):
    """
    質問に基づいて最も関連性の高い回答を返す関数
    """
    question = question.lower()

    for keyword, answer in qa_pairs.items():
        if keyword in question:
            return answer
    return "申し訳ありませんが、その質問にはお答えできません。別の質問をしてください。"

# チャットボットのUIコンポーネントを返すエンドポイント
@app.route('/chatbot_ui')
def chatbot_ui():
    """
    チャットボットのUIコンポーネント（HTML）を返す
    """
    # templates/chatbot_ui.html を新しく作成します
    return render_template('chatbot_ui.html')

# ユーザーからの質問を受け取り、回答を返すAPIエンドポイント
@app.route('/ask', methods=['POST'])
def ask_chatbot():
    """
    ユーザーからの質問を受け取り、回答を返すAPIエンドポイント
    """
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'answer': '質問が空です。'})
    
    bot_answer = get_answer(user_message)
    return jsonify({'answer': bot_answer})

if __name__ == '__main__':
    app.run(debug=True)