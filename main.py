# main.py
from flask import Flask, render_template, request, jsonify
from qa_data import qa_pairs # qa_data.py から qa_pairs をインポート

app = Flask(__name__)

def get_answer(question):
    """
    質問に基づいて最も関連性の高い回答を返す関数
    """
    question = question.lower()

    for keyword, answer in qa_pairs.items():
        if keyword in question:
            return answer
    return "申し訳ありませんが、その質問にはお答えできません。別の質問をしてください。"

@app.route('/')
def index():
    """
    チャットボットのメインページ（UI全体）を表示
    """
    return render_template('index.html') # templates/index.html をレンダリング

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
    app.run(debug=True) # 開発中は debug=True が便利
