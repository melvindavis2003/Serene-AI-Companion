import os
import tempfile
import base64
from flask import Flask, request, render_template, send_file, jsonify
from dotenv import load_dotenv

from gemini_service import process_audio_prompt, process_text_prompt
from tts_service import text_to_speech

load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process-audio", methods=["POST"])
def process_audio():
    try:
        if "audio" not in request.files:
            return jsonify({"error": "No audio file provided in request"}), 400

        audio_file = request.files["audio"]
        mime_type = audio_file.mimetype or "audio/webm"
        
        # Read raw audio bytes
        audio_bytes = audio_file.read()
        if not audio_bytes:
            return jsonify({"error": "Audio file is empty"}), 400

        print(f"[Serene Pipeline] Received audio ({len(audio_bytes)} bytes, mime: {mime_type})")

        # 1. Process audio directly with Gemini 2.5 Flash
        ai_response_text = process_audio_prompt(audio_bytes, mime_type=mime_type)
        print(f"[Serene Gemini Response]: {ai_response_text}")

        # 2. Convert response to speech audio
        audio_path = text_to_speech(ai_response_text)

        # 3. Read generated TTS audio to return base64 JSON or file
        with open(audio_path, "rb") as f:
            generated_audio_bytes = f.read()

        audio_b64 = base64.b64encode(generated_audio_bytes).decode("utf-8")

        return jsonify({
            "success": True,
            "text": ai_response_text,
            "audio_b64": audio_b64,
            "mime_type": "audio/mp3"
        })

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"[Error in /process-audio]: {e}")
        return jsonify({"error": f"An error occurred while processing your request: {str(e)}"}), 500

@app.route("/process-text", methods=["POST"])
def process_text():
    try:
        data = request.get_json() or {}
        text_prompt = data.get("text", "").strip()

        if not text_prompt:
            return jsonify({"error": "No text prompt provided"}), 400

        # 1. Gemini text response
        ai_response_text = process_text_prompt(text_prompt)

        # 2. TTS
        audio_path = text_to_speech(ai_response_text)

        with open(audio_path, "rb") as f:
            generated_audio_bytes = f.read()

        audio_b64 = base64.b64encode(generated_audio_bytes).decode("utf-8")

        return jsonify({
            "success": True,
            "text": ai_response_text,
            "audio_b64": audio_b64,
            "mime_type": "audio/mp3"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"Serene AI Companion Server starting on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
