# main.py
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Google Gemini API のインポート
import google.generativeai as genai

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からAPIキーを取得し、Gemini APIを設定
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY 環境変数が設定されていません。")
genai.configure(api_key=GOOGLE_API_KEY)# === 一時的なモデル確認コード：実行後、この部分は削除してください ===
print("--- 利用可能なGeminiモデル ---")
found_models = False
for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(f"- {m.name}")
        found_models = True
if not found_models:
    print("利用可能なGeminiモデルが見つかりませんでした。APIキーや地域設定を確認してください。")
print("-------------------------")
# =========================================================


app = Flask(__name__)

def get_gemini_answer(question):
    """
    Google Gemini APIを使用して質問に基づいて回答を生成する関数
    """
    try:
        # 使用するモデルを指定 (例: gemini-pro)
        model = genai.GenerativeModel('models/gemini-1.5-flash')




        # AIに質問を送信し、回答を生成
        response = model.generate_content(question)

        # 応答からテキストを抽出
        if response.parts:
            if hasattr(response, 'text'):
                return response.text.strip()
            elif response.parts and hasattr(response.parts[0], 'text'):
                return response.parts[0].text.strip()
        
        # contentがない場合（例: safety-settingsによるブロックなど）
        return "申し訳ありませんが、その質問にはお答えできませんでした。別の質問をしてください。"

    except Exception as e:
        print(f"Gemini APIエラー: {e}")
        return "申し訳ありませんが、現在AIが応答できません。しばらくしてから再度お試しください。"

@app.route('/')
def index():
    """
    チャットボットのメインページ（UI全体）を表示
    """
    return render_template('index.html') # templates/index.html をレンダリング

@app.route('/ask', methods=['POST'])
def ask_chatbot():
    """
    ユーザーからの質問を受け取り、AIが回答を返すAPIエンドポイント
    """
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'answer': '質問が空です。'})

    # Gemini AIを使って回答を生成
    bot_answer = get_gemini_answer(user_message)
    return jsonify({'answer': bot_answer})

if __name__ == '__main__':
    app.run(debug=True)
