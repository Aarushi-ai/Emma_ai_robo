"""
emma_controller.py  —  FINAL VERSION
--------------------------------------
- Uses new google.genai library (not deprecated google.generativeai)
- Model: gemini-2.5-flash-lite (confirmed working)
- State machine: LISTENING -> THINKING -> SPEAKING -> LISTENING
- Threaded listen so robot.step() never blocks
- Commands: wave, left arm, right arm, both arms, dance
- pyttsx3 primary TTS, gTTS fallback
"""

import json
import os
import math
import threading
import time
import pygame
from google import genai
from controller import Robot
from dotenv import load_dotenv

try:
    import vosk, pyaudio
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    print("[INFO] vosk/pyaudio not installed — keyboard mode")

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    print("[WARN] pyttsx3 not installed")

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


# ── ENV ────────────────────────────────────────────────────────
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=env_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

CONTROLLER_DIR  = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR   = os.path.join(CONTROLLER_DIR, "..", "..", "Resources")
VOSK_MODEL_PATH = os.path.join(RESOURCES_DIR, "vosk-model-en-us-0.22")
LISTEN_SOUND    = os.path.join(RESOURCES_DIR, "listen.mp3")
CONVERT_SOUND   = os.path.join(RESOURCES_DIR, "convert.mp3")

GEMINI_MODEL = "models/gemini-2.5-flash-lite"


# ── GEMINI INIT ────────────────────────────────────────────────
_gemini_client = None

def _init_gemini():
    global _gemini_client
    if not GEMINI_API_KEY:
        print("[WARN] No GEMINI_API_KEY in .env file")
        return
    try:
        print(f"[...] Connecting to Gemini ({GEMINI_MODEL})...")
        _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        r = _gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents="say hi in 3 words"
        )
        print(f"[OK] Gemini ready: {r.text.strip()}")
    except Exception as e:
        print(f"[ERROR] Gemini failed: {e}")
        _gemini_client = None

_init_gemini()


# ── WEBOTS ─────────────────────────────────────────────────────
robot     = Robot()
TIME_STEP = int(robot.getBasicTimeStep())

left_motor  = robot.getDevice("left arm motor")
right_motor = robot.getDevice("right arm motor")
head_motor  = robot.getDevice("head motor")

for name, dev in [("left arm motor",  left_motor),
                  ("right arm motor", right_motor),
                  ("head motor",      head_motor)]:
    if dev is None:
        print(f"[ERROR] Motor '{name}' not found in .wbt!")
    else:
        dev.setVelocity(1.0)
        print(f"[OK] {name}")


# ── ANGLES ─────────────────────────────────────────────────────
def arm_rad(deg):
    return max(0.0, min(math.pi, math.radians(float(deg))))

def head_rad(deg):
    return max(-math.pi/2, min(math.pi/2, math.radians(float(deg) - 90.0)))

_deg = {"left": 180.0, "right": 0.0, "head": 90.0}

def move_to(left_deg=None, right_deg=None, head_deg=None, steps=40):
    if left_deg  is not None: _deg["left"]  = float(left_deg)
    if right_deg is not None: _deg["right"] = float(right_deg)
    if head_deg  is not None: _deg["head"]  = float(head_deg)
    left_motor.setPosition(arm_rad(_deg["left"]))
    right_motor.setPosition(arm_rad(_deg["right"]))
    head_motor.setPosition(head_rad(_deg["head"]))
    for _ in range(steps):
        if robot.step(TIME_STEP) == -1:
            break

def home():
    move_to(left_deg=180, right_deg=0, head_deg=90, steps=30)


# ── GESTURES ───────────────────────────────────────────────────
def hello_gesture():
    print("[Gesture] Wave hello")
    move_to(right_deg=180, steps=35)
    for _ in range(3):
        move_to(right_deg=150, steps=18)
        move_to(right_deg=180, steps=18)
    move_to(right_deg=0, steps=35)
    home()

def left_arm_gesture():
    print("[Gesture] Left arm raise")
    move_to(left_deg=90, steps=35)
    time.sleep(0.3)
    move_to(left_deg=180, steps=35)
    home()

def right_arm_gesture():
    print("[Gesture] Right arm raise")
    move_to(right_deg=90, steps=35)
    time.sleep(0.3)
    move_to(right_deg=0, steps=35)
    home()

def both_arms_gesture():
    print("[Gesture] Both arms up")
    move_to(left_deg=90, right_deg=180, steps=40)
    time.sleep(0.5)
    home()

def dance_gesture():
    print("[Gesture] Dance!")
    for _ in range(3):
        move_to(left_deg=90,  right_deg=180, head_deg=100, steps=15)
        move_to(left_deg=180, right_deg=0,   head_deg=80,  steps=15)
    home()

def thinking_gesture():
    move_to(head_deg=105, steps=18)
    move_to(head_deg=75,  steps=18)
    move_to(head_deg=90,  steps=15)

def nod_once():
    move_to(head_deg=100, steps=10)
    move_to(head_deg=82,  steps=10)
    move_to(head_deg=90,  steps=8)


# ── AUDIO ──────────────────────────────────────────────────────
pygame.mixer.init()

def play_sound(path):
    if os.path.exists(path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"[Sound] {e}")


# ── TTS ────────────────────────────────────────────────────────
def speak(text):
    print(f"\n[Emma] {text}\n")

    if PYTTSX3_AVAILABLE:
        try:
            done = threading.Event()

            def _say():
                try:
                    engine = pyttsx3.init()
                    voices = engine.getProperty('voices')
                    if len(voices) > 1:
                        engine.setProperty('voice', voices[1].id)
                    engine.setProperty('rate', 175)
                    engine.setProperty('volume', 1.0)
                    engine.say(text)
                    engine.runAndWait()
                except Exception as e:
                    print(f"[TTS] {e}")
                finally:
                    done.set()

            threading.Thread(target=_say, daemon=True).start()

            max_nods = max(1, len(text) // 40)
            nods = 0
            while not done.is_set() and nods < max_nods:
                nod_once()
                nods += 1
            done.wait(timeout=20)
            home()
            return
        except Exception as e:
            print(f"[pyttsx3] {e}")

    if GTTS_AVAILABLE:
        try:
            import tempfile
            tts = gTTS(text=text, lang='en', slow=False)
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tmp.close()
            tts.save(tmp.name)
            pygame.mixer.music.load(tmp.name)
            pygame.mixer.music.play()
            max_nods = max(1, len(text) // 40)
            nods = 0
            while pygame.mixer.music.get_busy() and nods < max_nods:
                nod_once()
                nods += 1
            pygame.mixer.music.stop()
            try: os.unlink(tmp.name)
            except: pass
            home()
            return
        except Exception as e:
            print(f"[gTTS] {e}")

    print(f"[No TTS] {text}")
    home()


# ── VOSK ───────────────────────────────────────────────────────
vosk_model = None
if VOSK_AVAILABLE:
    if os.path.exists(VOSK_MODEL_PATH):
        print(f"[OK] Loading VOSK...")
        vosk_model = vosk.Model(VOSK_MODEL_PATH)
        print("[OK] VOSK ready — speak to Emma!")
    else:
        print("[INFO] VOSK model not found — KEYBOARD mode")
else:
    print("[INFO] KEYBOARD mode — type in the console")


# ── LISTEN THREADS ─────────────────────────────────────────────
heard_text    = None
hear_lock     = threading.Lock()
_listen_alive = False


def _vosk_thread():
    global heard_text, _listen_alive
    kaldi  = vosk.KaldiRecognizer(vosk_model, 16000)
    mic    = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1,
                      rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    try:
        while _listen_alive:
            data = stream.read(8192, exception_on_overflow=False)
            if not data:
                continue
            if kaldi.AcceptWaveform(data):
                result = json.loads(kaldi.Result())["text"].strip()
                if result:
                    print(f"[You said] {result}")
                    with hear_lock:
                        heard_text = result
                    break
    finally:
        stream.stop_stream()
        stream.close()
        mic.terminate()
        _listen_alive = False


def _keyboard_thread():
    global heard_text, _listen_alive
    print("\n>>> Type your message and press Enter: ", end="", flush=True)
    text = input().strip()
    with hear_lock:
        heard_text = text
    _listen_alive = False


def start_listening():
    global heard_text, _listen_alive
    heard_text    = None
    _listen_alive = True
    print("[Listening...]")
    if vosk_model:
        play_sound(LISTEN_SOUND)
        threading.Thread(target=_vosk_thread, daemon=True).start()
    else:
        threading.Thread(target=_keyboard_thread, daemon=True).start()


def get_input():
    global heard_text
    with hear_lock:
        if heard_text is not None:
            t = heard_text
            heard_text = None
            return t
    return None


# ── GEMINI CALL ────────────────────────────────────────────────
def ask_gemini(text):
    if _gemini_client is None:
        return "I cannot connect to my brain right now. Please check the API key."
    try:
        prompt = (
            "You are Emma, a friendly AI robot assistant. "
            "Reply in 1 to 2 short sentences only. Be warm and concise. "
            f"User said: {text}"
        )
        r = _gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return r.text.strip()
    except Exception as e:
        print(f"[Gemini] {e}")
        return "Sorry, I had a brain glitch! Please try again."


# ── COMMAND HANDLER ────────────────────────────────────────────
def handle_command(text):
    """Handle gesture commands locally. Returns True if handled."""
    t = text.lower().strip()

    # Wave / hello
    if any(w in t for w in ["wave", "say hi", "wave hi", "greet"]):
        speak("Hi there! Great to meet you!")
        hello_gesture()
        return True

    # Simple hi/hello — wave and greet
    if t in ["hi", "hello", "hey", "hi emma", "hello emma", "hey emma"]:
        speak("Hello! It is so nice to see you!")
        hello_gesture()
        return True

    # Left arm
    if any(w in t for w in ["left arm", "raise left", "move left", "left hand"]):
        speak("Sure! Here is my left arm!")
        left_arm_gesture()
        return True

    # Right arm
    if any(w in t for w in ["right arm", "raise right", "move right", "right hand"]):
        speak("Here is my right arm!")
        right_arm_gesture()
        return True

    # Both arms
    if any(w in t for w in ["both arms", "raise arms", "hands up", "both hands"]):
        speak("Both arms up!")
        both_arms_gesture()
        return True

    # Dance
    if any(w in t for w in ["dance", "do a dance", "dancing"]):
        speak("Let me show you my moves!")
        dance_gesture()
        return True

    # Name
    if any(w in t for w in ["your name", "who are you", "what are you"]):
        speak("I am Emma, your personal AI robot!")
        return True

    # Time
    if any(w in t for w in ["what time", "current time"]):
        now = time.strftime("%I:%M %p")
        speak(f"The current time is {now}.")
        return True

    return False


# ── STARTUP ────────────────────────────────────────────────────
print("\n" + "="*50)
print("  Emma AI Robot — Final Version")
print("="*50 + "\n")

robot.step(TIME_STEP)
home()
hello_gesture()
speak("Hello! I am Emma, your personal AI robot. How can I help you today?")
start_listening()


# ── MAIN LOOP ──────────────────────────────────────────────────
while robot.step(TIME_STEP) != -1:

    user_input = get_input()

    if user_input is None:
        continue

    if not user_input.strip():
        start_listening()
        continue

    if handle_command(user_input):
        start_listening()
    else:
        print(f"[Thinking] {user_input}")
        thinking_gesture()
        response = ask_gemini(user_input)
        speak(response)
        start_listening()