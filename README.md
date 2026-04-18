# 🤖 Emma — AI-Powered Humanoid Robot

Emma is an AI-powered humanoid robot that can **listen**, **think**, and **speak** — combining servo-controlled physical movement with real-time AI conversation. Built with Python, Arduino, and Google Gemini, Emma is a fully integrated human-robot interaction system built from scratch.

> ⚙️ **Status:** Software complete. Physical assembly in progress.

---

## 🧠 What Emma Can Do

| Capability | Technology |
|---|---|
| 🎙️ Hear you | VOSK (offline) or Google Speech API (online) |
| 🤖 Understand & respond | Google Gemini 2.5 Flash |
| 🔊 Speak back | OpenAI TTS (online) or pyttsx3 (offline) |
| 💪 Move arms & head | Arduino + 3x Servo Motors via cvzone |
| 👋 Wave hello | Smooth servo interpolation gesture |

---

## 📁 Project Structure

```
Emma_ai_robo/
│
├── hardware/
│   ├── Emma.ino                      # Arduino sketch — receives servo angles over serial
│   ├── servos_basic.py               # Smooth servo movement with interpolation
│   └── hello_emma.py                 # "Hello" wave gesture script
│
├── software/
│   ├── speech_to_text.py             # Online STT — Google Speech Recognition API
│   ├── speech_to_text_offline.py     # Offline STT — VOSK
│   ├── ai_model.py                   # AI response generation — Google Gemini API
│   ├── text_to_speech.py             # Online TTS — OpenAI
│   ├── text_to_speech_offline.py     # Offline TTS — pyttsx3
│   └── main.py                       # Full pipeline: Listen → Think → Speak
│
├── Resources/
│   ├── listen.mp3                    # Audio feedback: "listening" chime
│   ├── convert.mp3                   # Audio feedback: "processing" chime
│   └── vosk-model-en-us-0.22/        # VOSK offline model (download separately)
│
├── .env.example                      # API key template — copy to .env
├── .gitignore                        # Excludes .env, __pycache__, etc.
├── requirements.txt                  # Python dependencies
└── README.md                         # You are here
```

---

## ⚡ How It Works

```
┌─────────────┐
│  Microphone │
└──────┬──────┘
       │ raw audio
       ▼
┌─────────────────────────┐
│   Speech-to-Text        │  ← speech_to_text_offline.py  (VOSK)
│                         │  ← speech_to_text.py          (Google API)
└──────┬──────────────────┘
       │ text string
       ▼
┌─────────────────────────┐
│   AI Language Model     │  ← ai_model.py  (Google Gemini 2.5 Flash)
└──────┬──────────────────┘
       │ response text
       ▼
┌─────────────────────────┐
│   Text-to-Speech        │  ← text_to_speech.py          (OpenAI TTS)
│                         │  ← text_to_speech_offline.py  (pyttsx3)
└──────┬──────────────────┘
       │ audio bytes
       ▼
┌─────────────┐     ┌──────────────────────────────┐
│   Speaker   │     │   Servo Motors (Arduino)     │
└─────────────┘     │   servos_basic.py             │
                    │   hello_emma.py               │
                    └──────────────────────────────┘
```

---

## 🛠️ Hardware Requirements

| Component | Details |
|---|---|
| Microcontroller | Arduino Uno or Mega |
| Servo Motors | 3× (Left Arm, Right Arm, Head) |
| Microphone | USB or 3.5mm |
| Speaker | USB or 3.5mm |
| Computer | Windows / Linux / Mac running Python 3.10+ |

**Servo Pin Mapping (Arduino):**

| Servo | Pin | Default Angle |
|---|---|---|
| Left Arm (LServo) | D8 | 180° |
| Right Arm (RServo) | D9 | 0° |
| Head (HServo) | D10 | 90° |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Aarushi-ai/Emma_ai_robo.git
cd Emma_ai_robo
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Activate on Linux/Mac:
source .venv/bin/activate

# Activate on Windows:
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up API keys

```bash
# Copy the template
cp .env.example .env
```

Open `.env` and fill in your keys:

```
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
```

> 🔑 Get Gemini key: https://ai.google.dev/gemini-api/docs/api-key
> 🔑 Get OpenAI key: https://platform.openai.com/api-keys

### 5. Download the VOSK model (for offline speech recognition)

Download from: https://alphacephei.com/vosk/models

Recommended: `vosk-model-en-us-0.22`

Place the extracted folder inside `Resources/`:
```
Resources/
└── vosk-model-en-us-0.22/
```

### 6. Upload Arduino sketch

Open `hardware/Emma.ino` in the Arduino IDE and upload it to your Arduino board.

### 7. Run Emma

```bash
# Test servo movement
python hardware/servos_basic.py

# Test hello gesture
python hardware/hello_emma.py

# Run full AI pipeline
python software/main.py
```

---

## 📦 Dependencies

```
# Hardware / Arduino communication
cvzone
pyserial

# Speech Recognition
SpeechRecognition
pyaudio
vosk

# Text-to-Speech (online)
openai
pygame

# Text-to-Speech (offline)
pyttsx3

# AI Language Model
google-generativeai

# Environment / API key management
python-dotenv
```

See `requirements.txt` for pinned versions.

---

## 🔒 API Key Security

**Never hardcode API keys into your source files.** Emma uses a `.env` file to keep keys out of the codebase.

- `.env` is listed in `.gitignore` and will never be committed to GitHub
- Use `.env.example` as a safe template to share the key structure without exposing real values
- If you accidentally committed a key, **revoke it immediately** at the provider dashboard and generate a new one

---

## 🗺️ Roadmap

- [x] Servo motor control with smooth interpolation
- [x] Hello wave gesture
- [x] Speech-to-text — online (Google API)
- [x] Speech-to-text — offline (VOSK)
- [x] Text-to-speech — online (OpenAI)
- [x] Text-to-speech — offline (pyttsx3)
- [x] AI model integration (Gemini)
- [x] Full pipeline integration (`main.py`)
- [ ] Physical robot assembly
- [ ] Face tracking with camera
- [ ] Demo video / simulation
- [ ] Wake word detection ("Hey Emma")

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Aarushi** — [@Aarushi-ai](https://github.com/Aarushi-ai)

Emma is a personal robotics project combining AI, hardware, and human-robot interaction — built entirely from scratch.
