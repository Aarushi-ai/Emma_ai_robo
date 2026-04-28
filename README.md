# Emma — AI-Powered Humanoid Robot

Emma is a humanoid robot built from scratch, combining offline and online AI capabilities with physical servo-based movement. She can listen to speech, generate intelligent responses via Gemini AI, speak back using text-to-speech, and move her arms — all in a unified pipeline. A Webots-based simulation environment is currently under active development.

**Current Status**

| Component | Status |
|---|---|
| AI + Voice Pipeline | Complete |
| Arduino Servo Control | Complete |
| Webots Simulation | Basic — refinement in progress |
| Physical Assembly | In progress |

---

## Capabilities

| Feature | Technology |
|---|---|
| Speech Recognition (Online) | Google Speech API |
| Speech Recognition (Offline) | VOSK |
| AI Response Generation | Google Gemini 2.5 Flash |
| Text-to-Speech (Online) | OpenAI TTS |
| Text-to-Speech (Offline) | pyttsx3 |
| Arm Movement | Arduino + 3x Servo Motors via cvzone |
| Simulation | Webots |

---

## Project Structure

```
Emma_ai_robo/
│
├── hardware/
│   ├── Emma_Robo.ino                  # Arduino sketch for servo control
│   ├── servos_basic.py                # Servo movement with smooth interpolation
│   └── hello_emma.py                  # Hello wave gesture
│
├── software/
│   ├── speech_to_text.py              # Online speech-to-text (Google API)
│   ├── speech_to_text_offline.py      # Offline speech-to-text (VOSK)
│   ├── ai_model.py                    # AI response generation (Gemini)
│   ├── text_to_speech.py              # Online text-to-speech (OpenAI)
│   ├── text_to_speech_offline.py      # Offline text-to-speech (pyttsx3)
│   ├── ai_speech_integration.py       # Full pipeline — AI + voice + movement
│   └── main.py                        # Software only — AI + voice, no Arduino
│
├── my_project/                        # Webots Simulation (in progress)
│   ├── controllers/
│   │   └── emma_controller/
│   │       └── emma_controller.py     # Emma's simulation controller
│   ├── worlds/
│   │   └── emma_robo.wbt              # Webots world file
│   ├── libraries/
│   ├── plugins/
│   │   ├── physics/
│   │   ├── remote_controls/
│   │   └── robot_windows/
│   ├── protos/
│   └── Resources/
│       └── vosk-model-en-us-0.22/     # VOSK model (download separately)
│
├── .env.example                       # API key template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Aarushi-ai/Emma_ai_robo.git
cd Emma_ai_robo
```

### 2. Set up a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

```bash
cp .env.example .env
```

Open `.env` and fill in your keys:

```
GEMINI_API_KEY=your_gemini_key_here
OPENAI_API_KEY=your_openai_key_here
```

- Gemini API key: https://ai.google.dev/gemini-api/docs/api-key
- OpenAI API key: https://platform.openai.com/api-keys

### 5. Download the VOSK model (offline speech only)

Download `vosk-model-en-us-0.22` from https://alphacephei.com/vosk/models and place the extracted folder in:
- `software/` for the main pipeline
- `my_project/Resources/` for the Webots simulation

> The model is not included in this repository due to its size.

### 6. Upload the Arduino sketch

Open `hardware/Emma_Robo.ino` in Arduino IDE and upload it to your board.

---

## Running Emma

| Script | Arduino Required | Description |
|---|---|---|
| `software/main.py` | No | AI + voice only |
| `software/ai_speech_integration.py` | Yes | Full pipeline — AI + voice + movement |
| `hardware/servos_basic.py` | Yes | Test servo movement |
| `hardware/hello_emma.py` | Yes | Test hello wave gesture |

```bash
# Run software-only mode
python software/main.py

# Run full robot mode
python software/ai_speech_integration.py
```

---

## Webots Simulation

A simulation environment for Emma is being developed in Webots. The basic simulation is functional — Emma's robot model loads in the world and the controller runs. Work is ongoing to refine movement accuracy, behaviour logic, and sensor integration.

### Requirements

- [Webots](https://cyberbotics.com/) R2023b or later
- Python 3.10+

### Running the Simulation

1. Open Webots
2. Go to **File → Open World**
3. Select `my_project/worlds/emma_robo.wbt`
4. Press **Play**

Emma's behaviour in simulation is controlled by `my_project/controllers/emma_controller/emma_controller.py`.

**What works:** Robot loads, controller runs, basic motion executes.  
**In progress:** Movement smoothing, behaviour refinement, full AI integration in simulation.

---

## Hardware

| Component | Detail |
|---|---|
| Microcontroller | Arduino Uno / Mega |
| Servo Motors | 3x (Left Arm, Right Arm, Head) |
| Microphone | USB or 3.5mm |
| Speaker | USB or 3.5mm |
| Computer | Python 3.10+ |

**Servo Pin Mapping**

| Servo | Pin | Default Angle |
|---|---|---|
| Left Arm | D8 | 180° |
| Right Arm | D9 | 0° |
| Head | D10 | 90° |

---

## Dependencies

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
python-dotenv       # Environment variable management
```

---

## API Key Safety

- API keys are stored in `.env` which is listed in `.gitignore` and never pushed to GitHub
- `.env.example` is a safe public template — it contains no real keys
- If a key is accidentally exposed, revoke it immediately from the provider dashboard

---

## Roadmap

- [x] Servo motor control
- [x] Hello wave gesture
- [x] Speech-to-text — online and offline
- [x] Text-to-speech — online and offline
- [x] Gemini AI integration
- [x] Full software pipeline — `main.py`
- [x] Full robot integration — `ai_speech_integration.py`
- [x] Webots simulation — basic setup complete
- [ ] Webots simulation — movement smoothing and refinement
- [ ] Webots simulation — full AI behaviour integration
- [ ] Physical robot assembly
- [ ] Face tracking with camera
- [ ] Wake word detection — "Hey Emma"
- [ ] Demo video

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Aarushi** · [@Aarushi-ai](https://github.com/Aarushi-ai)

*Emma is a personal robotics project exploring the intersection of AI, voice interaction, and physical hardware — built entirely from scratch.*
