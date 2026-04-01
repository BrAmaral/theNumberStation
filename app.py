from flask import Flask, render_template, request, jsonify, send_file
import secrets
import io
import numpy as np
import soundfile as sf
from datetime import datetime, timezone

# --- KOKORO TTS ENGINE INITIALIZATION ---
try:
    from kokoro import KPipeline
    pipeline = KPipeline(lang_code='a')
    KOKORO_AVAILABLE = True
except ImportError:
    KOKORO_AVAILABLE = False

app = Flask(__name__)

# The 100-character alphabet (Indices 00-99)
ALPHABET = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    "abcdefghijklmnopqrstuvwxyz" 
    "0123456789"                  
    " .,!?-+/():; '\"\n\t_@#*&%=$" 
    "<>[]{}|\\^~`\r\x0b\x0c"       
)

# PROTOCOL OFFSETS (Strict 5-unit increments)
PROTOCOLS = {
    "ASCENSION": 0,
    "VORKUTA": 5,
    "ECHELON": 10,
    "RAINBOW": 15,
    "PHOENIX": 20
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        length = int(request.json.get('length', 500))
        pad = [f"{secrets.randbelow(100):02}" for _ in range(length)]
        return jsonify({"pad": " ".join(pad)})
    except Exception:
        return jsonify({"error": "GENERATOR_FAILURE"}), 500

@app.route('/broadcast', methods=['POST'])
def broadcast():
    data = request.json
    msg = data.get('message', '')
    pad_str = data.get('pad', '').split()
    protocol_name = data.get('protocol', '').upper()
    
    if protocol_name not in PROTOCOLS:
        return jsonify({"error": "INVALID_PROTOCOL_SELECTION"}), 400

    try:
        offset = PROTOCOLS[protocol_name]
        pad_values = [int(n) for n in pad_str]
        indices = [ALPHABET.index(c) for c in msg if c in ALPHABET]
        
        active_pad = pad_values[offset : offset + len(indices)]
        
        if len(indices) > len(active_pad):
            return jsonify({"error": f"PAD_DEPTH_INSUFFICIENT_FOR_{protocol_name}"}), 400
            
        # Cipher Math: (P + K) mod 100
        ciphertext = [(m + p) % 100 for m, p in zip(indices, active_pad)]
        zulu_time = datetime.now(timezone.utc).strftime('%H:%M:%SZ')
        
        formatted_cipher = " ".join([f"{n:02}" for n in ciphertext])
        return jsonify({
            "result": f"{protocol_name} {formatted_cipher}",
            "timestamp": zulu_time,
            "origin": protocol_name
        })
    except Exception:
        return jsonify({"error": "ENCODE_CORRUPTION"}), 400

@app.route('/decode', methods=['POST'])
def decode():
    data = request.json
    raw_input = data.get('message', '').strip().split()
    pad_str = data.get('pad', '').split()
    
    if not raw_input:
        return jsonify({"error": "NO_DATA_RECEIVED"}), 400

    protocol_name = raw_input[0].upper()
    cipher_str = raw_input[1:] 
    
    if protocol_name not in PROTOCOLS:
        return jsonify({"error": f"UNKNOWN_PROTOCOL:_{protocol_name}"}), 400
    
    try:
        offset = PROTOCOLS[protocol_name]
        cipher_values = [int(n) for n in cipher_str]
        pad_values = [int(n) for n in pad_str]
        
        active_pad = pad_values[offset : offset + len(cipher_values)]
        
        if len(cipher_values) > len(active_pad):
            return jsonify({"error": "PAD_WINDOW_MISMATCH"}), 400
            
        # Decipher Math: (C - K) mod 100
        decoded_indices = [(c - p) % 100 for c, p in zip(cipher_values, active_pad)]
        plaintext = "".join([ALPHABET[i] for i in decoded_indices])
        
        zulu_time = datetime.now(timezone.utc).strftime('%H:%M:%SZ')
        return jsonify({
            "result": plaintext,
            "timestamp": zulu_time,
            "origin": f"SECURE_DECRYPT_{protocol_name}"
        })
    except Exception:
        return jsonify({"error": "DECRYPTION_FAILURE"}), 400

@app.route('/synthesize', methods=['POST'])
def synthesize():
    if not KOKORO_AVAILABLE:
        return jsonify({"error": "KOKORO_ENGINE_OFFLINE"}), 501
    
    data = request.json
    text = data.get('text', '')
    
    # 1. Split the message into individual "calls" (Protocol + Numbers)
    parts = text.split()
    
    try:
        sample_rate = 24000
        # 2. Define your silence duration (e.g., 1.5 seconds)
        # Formula: duration_in_seconds * sample_rate
        silence_segment = np.zeros(int(0.5 * sample_rate), dtype=np.float32)
        
        final_audio_segments = []

        for i, part in enumerate(parts):
            # Generate audio for just this one word/number
            # Speed 0.8 is usually better for clarity when using segments
            generator = pipeline(part, voice='bf_emma', speed=1)
            
            # Extract the audio array from the generator
            for _, _, audio in generator:
                final_audio_segments.append(audio)
            
            # Add silence after every part except the very last one
            if i < len(parts) - 1:
                final_audio_segments.append(silence_segment)
        
        # 3. Concatenate everything into one master broadcast
        full_audio = np.concatenate(final_audio_segments)
        
        byte_io = io.BytesIO()
        sf.write(byte_io, full_audio, sample_rate, format='WAV')
        byte_io.seek(0)
        
        return send_file(byte_io, mimetype="audio/wav")
    except Exception as e:
        print(f"Synthesis Error: {e}")
        return jsonify({"error": "AUDIO_SYNTHESIS_FAILED"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)