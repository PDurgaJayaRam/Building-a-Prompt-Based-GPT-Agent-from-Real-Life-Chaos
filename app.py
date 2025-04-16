from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv
import os
import traceback

# Load environment variables from .env file
load_dotenv()

# Configure OpenAI client using environment variables
openai.api_base = os.getenv("OPENAI_API_BASE_URL")
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question')
        structured_data = data.get('structuredData')
        prompt_instructions = data.get('promptInstructions')
        
        if not question or not structured_data or not prompt_instructions:
            return jsonify({"error": "Missing required parameters"}), 400
        
        # Combine structured data and prompt instructions into a context
        context = f"Context:\n{prompt_instructions}\n\n{structured_data}\n\nQuestion: {question}"
        
        # Call OpenAI API using the updated client
        client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE_URL")
        )
        
        response = client.chat.completions.create(
            model="gpt-4o",  # Replace with your model
            messages=[
                {"role": "system", "content": prompt_instructions},
                {"role": "user", "content": context}
            ]
        )
        
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        # Log the full traceback for debugging
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)