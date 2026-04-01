# 📟 theNumberStation

theNumberStation is a mathematically "perfect" communication terminal designed to replicate the haunting, rhythmic broadcasts of Cold War-era **Numbers Stations**. Utilizing a **One-Time Pad (OTP)** cipher, the terminal ensures that messages are information-theoretically secure, rendered in a high-fidelity **Amber-P3 Phosphor** aesthetic.

> ### ⚠️ DISCLAIMER
> **FOR SIMULATION PURPOSES ONLY.** This project was developed as a thematic and educational exercise ("for fun"). While the underlying mathematics of the One-Time Pad are cryptographically sound, this implementation has not been audited for high-stakes security environments. Do not use this software for the transmission of sensitive, real-world data or in life-critical situations.


## 🛠 KEY FEATURES

* **Information-Theoretic Security:** Uses a 1:1 ratio between a 100-character alphabet and a 00-99 random pad.
* **British "Voice of the Station":** Integrated **Kokoro-82M TTS** engine (Voice: `bf_emma`) that reads transmissions with a slow, rhythmic British cadence.
* **Protocol Pointer System:** Implements functional offsets (**ASCENSION**, **VORKUTA**, etc.) to allow multiple messages to exist on a single Master Pad without key reuse.
* **Amber-P3 UI:** A gritty, flickering monochrome interface with authentic CRT scanlines and voltage-drop animations.
* **Automatic Data Purge:** A 30-second "Burn After Reading" volatile memory wipe for all decoded intercepts.
* **Dockerized Infrastructure:** Fully containerized for rapid deployment in isolated environments.

## 🔐 CRYPTOGRAPHIC SPECIFICATIONS

The terminal operates on **Modular Arithmetic** over a fixed 100-character space.

* **Alphabet:** `A-Z, a-z, 0-9, .,!?-+/():; '\" \n \t _@#*&%=$ <>[]{}|\\^~`
* **Encryption:** $C = (P + K) \pmod{100}$
* **Decryption:** $P = (C - K) \pmod{100}$
* **Randomness:** Powered by Python's `secrets` module, utilizing OS-level entropy for unpredictable pad generation.

## 🚀 INSTALLATION & DEPLOYMENT

### 🐋 Option A: Docker (Recommended)
The Docker build includes all system dependencies for audio synthesis (like `espeak-ng`) and pre-downloads the Kokoro-82M model.

1.  **Build the Image:**
    ```bash
    docker build -t echelon-terminal .
    ```
2.  **Launch the Tool:**
    ```bash
    docker run -d -p 5000:5000 --name strategic_terminal echelon-terminal
    ```
3.  **Access:** Navigate to `http://localhost:5000` in your browser.

### 🐍 Option B: Local Manual Setup
1.  **Dependencies:** Ensure you are using **Python 3.10, 3.11, or 3.12**.
2. **Create virtual environment**
    ```
    python -m venv venv && source venv/bin/activate
    ```
2.  **Install Requirements:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run:**
    ```bash
    python app.py
    ```

---

## 📡 OPERATIONAL PROTOCOLS

To prevent **Many-Time Pad** attacks, always use the Protocol Offset system to shift the "window" of your Master Pad.

| Protocol | Offset | Notes |
| :--- | :--- | :--- |
| **ASCENSION** | 000 | Baseline Offset |
| **VORKUTA** | 005 | Level 1 Shift |
| **ECHELON** | 010 | Level 2 Shift |
| **RAINBOW** | 015 | Level 3 Shift |
| **PHOENIX** | 020 | Emergency Shift |

**Rule of Five:** If a message is longer than 5 characters, you must skip the next protocol in the sequence to ensure pad windows do not overlap.

---

## 📦 REQUIREMENTS

* **Flask:** Web framework.
* **Kokoro:** High-quality neural TTS.
* **Soundfile / Numpy:** Audio processing and modular math.
* **Espeak-ng:** Required on the host system for British phonemization.

---

**"THE NUMBERS, MASON. WHAT DO THEY MEAN?"**