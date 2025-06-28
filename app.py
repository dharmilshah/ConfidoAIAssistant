from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import os
from prompts import SYSTEM_PROMPT

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/retell-webhook", methods=["POST"])
def retell_webhook():
    data = request.json
    user_input = data.get("transcript", "")

    if not user_input:
        return jsonify({"response": "Sorry, I didn't catch that.", "end_call": False})

    try:
        # Simple call to OpenAI Chat Completion
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.5
        )

        reply = response['choices'][0]['message']['content'].strip()
        return jsonify({"response": reply, "end_call": False})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"response": "There was an error processing your request.", "end_call": False})

if __name__ == "__main__":
    app.run(port=5000)
