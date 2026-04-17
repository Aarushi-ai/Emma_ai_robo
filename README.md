# 🤖 Emma — AI-Powered Humanoid Robot

Emma is an AI-powered humanoid robot that can **listen**, **think**, and **speak** — combining servo-controlled physical movement with real-time AI conversation. Built with Python, Arduino, and a language model backend, Emma represents a fully integrated human-robot interaction system.

> ⚙️ **Status:** Software complete. Physical assembly in progress.

---

## 🧠 What Emma Can Do

- 🎙️ **Hear you** — Speech-to-text (online & offline modes)
- 🤖 **Understand & respond** — AI language model processes your input
- 🔊 **Speak back** — Text-to-speech output (online & offline modes)
- 💪 **Move** — Smooth servo-controlled arm and head gestures via Arduino
- 👋 **Greet** — Performs a "Hello" wave gesture

---

## 📁 Project Structure

```
Emma_ai_robo/
│
├── hardware/                        # Arduino & physical hardware control
│   ├── servos_basic.py              # Core servo movement with smooth interpolation
│   ├── hello_emma.py                # "Hello" wave gesture script
│   ├── text_to_speech.py            # Online TTS (Google TTS / ElevenLabs)
│   ├── text_to_speech_offline.py    # Offline TTS (pyttsx3)
│   └── ai_speech_integration.py    # Full listen→think→speak pipeline bridge
│
├── software/                        # AI & speech processing
│   ├── speech_to_text.py            # Online STT (Google Speech API)
│   ├── speech_to_text_offline.py   # Offline STT (Vosk / Whisper)
│   └── ai_model.py                  # AI language model integration
│
├── docs/                            # Documentation & diagrams (coming soon)
│
├── requirements.txt                 # Python dependencies
├── .gitignore                       # Files excluded from version control
└── README.md                        # You are here
```

---

## ⚡ How It Works

```
[ Microphone ]
      ↓
[ Speech-to-Text ]   ← speech_to_text.py / speech_to_text_offline.py
      ↓
[  AI Model     ]   ← ai_model.py  (processes language, generates response)
      ↓
[ Text-to-Speech ]  ← text_to_speech.py / text_to_speech_offline.py
      ↓
[   Speaker     ]
      +
[ Servo Motors  ]   ← servos_basic.py / hello_emma.py  (physical gestures)
```

---

## 🛠️ Hardware Requirements

| Component | Details |
|-----------|---------|
| Microcontroller | Arduino (Uno / Mega) |
| Servo Motors | 3x (Left Arm, Right Arm, Head) |
| Microphone | USB or 3.5mm mic |
| Speaker | USB / 3.5mm speaker |
| Computer | Windows/Linux PC running Python 3.12 |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Emma_ai_robo.git
cd Emma_ai_robo
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Connect Arduino & run
Upload your servo sketch to Arduino, then:
```bash
python hardware/servos_basic.py       # Test servo movement
python hardware/hello_emma.py        # Test hello gesture
```

---

## 📦 Dependencies

See [`requirements.txt`](requirements.txt) for full list. Key libraries:

- `cvzone` — Arduino serial communication for servo control
- `pyserial` — Serial port communication
- `SpeechRecognition` — Online speech-to-text
- `gTTS` / `pyttsx3` — Text-to-speech (online/offline)
- `openai` / `google-generativeai` — AI language model

---

## 🗺️ Roadmap

- [x] Servo motor control (smooth interpolation)
- [x] Hello wave gesture
- [x] Speech-to-text (online)
- [x] Speech-to-text (offline)
- [x] Text-to-speech (online)
- [x] Text-to-speech (offline)
- [x] AI model integration
- [x] Full pipeline integration script
- [ ] Physical robot assembly
- [ ] Online simulation / demo video
- [ ] Face tracking with camera

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Aarushi-ai**
- GitHub: [@Aarushi-ai](https://github.com/Aarushi-ai)

---

> *Emma is a personal robotics project combining AI, hardware, and human-robot interaction — built entirely from scratch.*
