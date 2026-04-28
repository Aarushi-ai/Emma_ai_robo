# 🤖 Emma — AI-Powered Humanoid Robot

> *She listens. She thinks. She speaks. She moves.*

Emma is a humanoid AI robot that can hear you, understand you, talk back to you — and wave hello.
Built from scratch with Python, Arduino, and cutting-edge AI APIs.
Now with a **Webots simulation** to test behaviour before physical deployment.

**Status:** Software complete · Webots simulation complete · Physical assembly in progress

---

## 🧠 What Emma Can Do

| Capability | Technology |
|---|---|
| 🎙️ Hear you | VOSK (offline) or Google Speech API (online) |
| 🤖 Understand & respond | Google Gemini 2.5 Flash |
| 🔊 Speak back | OpenAI TTS (online) or pyttsx3 (offline) |
| 💪 Move arms | Arduino + 3× Servo Motors via cvzone |
| 👋 Wave hello | Smooth servo interpolation gesture |
| 🌐 Simulated movement | Webots robot simulator |

---

## 📁 Project Structure

```
Emma_ai_robo/
│
├── hardware/
│   ├── Emma_Robo.ino                # Arduino sketch — controls servo motors
│   ├── servos_basic.py              # Smooth servo movement with interpolation
│   └── hello_emma.py                # Hello wave gesture
│
├── software/
│   ├── speech_to_text.py            # Online speech-to-text (Google API)
│   ├── speech_to_text_offline.py    # Offline speech-to-text (VOSK)
│   ├── ai_model.py                  # AI response generation (Gemini)
│   ├── text_to_speech.py            # Online text-to-speech (OpenAI)
│   ├── text_to_speech_offline.py    # Offline text-to-speech (pyttsx3)
│   ├── ai_speech_integration.py     # FULL ROBOT — AI + voice + servo movement
│   └── main.py                      # Software only — AI + voice, no Arduino needed
│
├── my_project/                      # 🆕 Webots Simulation
│   ├── controllers/
│   │   └── emma_controller/
│   │       └── emma_controller.py   # Emma's brain in simulation
│   ├── worlds/
│   │   └── emma_robo.wbt            # Webots world file
│   ├── libraries/                   # Custom Webots libraries
│   ├── plugins/                     # Webots plugins
│   │   ├── physics/
│   │   ├── remote_controls/
│   │   └── robot_windows/
│   ├── protos/                      # Custom robot proto models
│   └── Resources/
│       └── vosk-model-en-us-0.22/   # VOSK offline model (download separately)
│
├── .env.example                     # API key template
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

---

## ⚡ How It Works

```
  [ You speak ]
       ↓
  [ Speech-to-Text ]   →   speech_to_text.py / speech_to_text_offline.py
       ↓
  [ Gemini AI ]        →   ai_model.py
       ↓
  [ Text-to-Speech ]   →   text_to_speech.py / text_to_speech_offline.py
       ↓
  [ Speaker ]  +  [ Servo Motors — Emma moves! ]
```

---

## 🗂️ Which Script to Run?

| Script | Needs Arduino? | Does |
|---|---|---|
| `hardware/servos_basic.py` | ✅ Yes | Tests servo movement |
| `hardware/hello_emma.py` | ✅ Yes | Tests hello wave gesture |
| `software/main.py` | ❌ No | AI + voice only, no movement |
| `software/ai_speech_integration.py` | ✅ Yes | Full robot — AI + voice + movement |
| Webots → `my_project/worlds/emma_robo.wbt` | ❌ No | Simulated Emma in Webots |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Aarushi-ai/Emma_ai_robo.git
cd Emma_ai_robo
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Mac/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API keys

```bash
cp .env.example .env
```

Open `.env` and fill in:

```
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
```

Get your keys here:
- Gemini → https://ai.google.dev/gemini-api/docs/api-key
- OpenAI → https://platform.openai.com/api-keys

### 5. Download VOSK model (offline speech recognition)

Download `vosk-model-en-us-0.22` from https://alphacephei.com/vosk/models

Place the extracted folder inside:
- `software/` for the main pipeline
- `my_project/Resources/` for the Webots simulation

### 6. Upload Arduino sketch

Open `hardware/Emma_Robo.ino` in Arduino IDE and upload to your board.

### 7. Run Emma

```bash
# Software only (no Arduino needed)
python software/main.py

# Full robot (Arduino connected)
python software/ai_speech_integration.py
```

---

## 🌐 Webots Simulation

Emma now has a virtual simulation environment built in **Webots**, allowing her behaviour and movement to be tested without physical hardware.

### Requirements
- [Webots](https://cyberbotics.com/) R2023b or later
- Python 3.10+

### How to Run the Simulation

1. Open Webots
2. Go to **File → Open World**
3. Select `my_project/worlds/emma_robo.wbt`
4. Press **Play ▶**

Emma's controller (`my_project/controllers/emma_controller/emma_controller.py`) handles her simulated behaviour.

> **Note:** The VOSK speech model is not included in the repo due to its size. Download it separately (see step 5 above) and place it in `my_project/Resources/`.

---

## 🛠️ Hardware

| Component | Detail |
|---|---|
| Microcontroller | Arduino Uno / Mega |
| Servo Motors | 3× (Left Arm, Right Arm, Head) |
| Microphone | USB or 3.5mm |
| Speaker | USB or 3.5mm |
| Computer | Python 3.10+ |

**Servo Pin Mapping:**

| Servo | Pin | Default |
|---|---|---|
| Left Arm | D8 | 180° |
| Right Arm | D9 | 0° |
| Head | D10 | 90° |

---

## 📦 Dependencies

```
cvzone              # Arduino serial communication
pyserial            # Serial port
SpeechRecognition   # Online speech-to-text
pyaudio             # Microphone input
vosk                # Offline speech-to-text
openai              # TTS + API
pygame              # Audio playback
pyttsx3             # Offline TTS
google-generativeai # Gemini AI
python-dotenv       # API key management
```

---

## 🔒 API Key Safety

- Never paste real keys into code files
- `.env` is blocked by `.gitignore` — it will never be pushed to GitHub
- `.env.example` is the safe public template with no real keys
- If you accidentally expose a key, revoke it immediately at the provider dashboard

---

## 🗺️ Roadmap

- [x] Servo motor control
- [x] Hello wave gesture
- [x] Speech-to-text (online + offline)
- [x] Text-to-speech (online + offline)
- [x] Gemini AI integration
- [x] Full pipeline — `main.py`
- [x] Full robot integration — `ai_speech_integration.py`
- [x] Webots simulation — basic simulation complete
- [ ] Physical robot assembly
- [ ] Face tracking with camera
- [ ] Wake word — "Hey Emma"
- [ ] Full AI behaviour in Webots simulation
- [ ] Demo video

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Aarushi** · [@Aarushi-ai](https://github.com/Aarushi-ai)

*Emma is a personal robotics project combining AI, hardware, and human-robot interaction — built entirely from scratch.*
