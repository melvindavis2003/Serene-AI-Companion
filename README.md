# Serene — AI Emotional Companion

Serene is a voice-first AI emotional companion powered by **Google Gemini 2.5 Flash** for multimodal audio reasoning and **Edge-TTS** for natural speech synthesis.

---

## ✨ Features
* **Multimodal Audio Intelligence**: Accepts raw voice audio recordings directly from the browser. Google Gemini 2.5 Flash comprehends audio tone, emotion, and context in a single call.
* **Empathetic Companion Persona**: System prompts guide Gemini to act as a gentle, warm, and supportive conversational companion.
* **High-Quality Neural Speech Output**: Uses `edge-tts` (`en-US-AvaNeural`) to convert text responses into fluid, natural audio playback.
* **Modern Web Interface**: Responsive glassmorphism UI with real-time glowing voice orb, recording state animations, microphone soundwave visualizer, and backup text input.
* **Secure Environment Setup**: Zero hardcoded API keys; managed safely via `.env`.

---

## 📁 Repository Structure
```
├── app.py               # Main Flask web application server & routes
├── gemini_service.py    # Google Gemini 2.5 Flash audio & text companion integration
├── tts_service.py       # High-quality neural Text-to-Speech synthesis
├── templates/
│   └── index.html       # Glassmorphism UI with voice orb & recording controls
├── .env.example         # Environment configuration template
├── .env                 # API Key configuration
└── requirements.txt     # Python project dependencies
```

---

## 🚀 Quickstart Guide (Windows / Mac / Linux)

### 1. Prerequisites
Ensure Python is installed on your system.
* **On Windows**: Check if Python is installed by running: `py --version` or `python --version` in PowerShell / Command Prompt.
* If Python is missing on Windows, install it using winget:
  ```powershell
  winget install Python.Python.3.12
  ```

### 2. Install Dependencies

**Windows (PowerShell / Command Prompt)**:
```powershell
py -m pip install -r requirements.txt
```
*(or `python -m pip install -r requirements.txt`)*

**Mac / Linux**:
```bash
python3 -m pip install -r requirements.txt
```

### 3. Configure Gemini API Key
Obtain a free API key from [Google AI Studio](https://aistudio.google.com/).

Create/update your `.env` file:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
PORT=8080
```

### 4. Run the Server

**Windows (PowerShell / Command Prompt)**:
```powershell
py app.py
```
*(or `python app.py`)*

**Mac / Linux**:
```bash
python3 app.py
```

Open your web browser and navigate to `http://localhost:8080` to start talking with **Serene**.
