"""
Single-service server for the Azerbaijani rule-based TTS demo.

Serves:
  GET  /          → Next.js static frontend (built into /app/static/)
  GET  /health    → JSON health check
  POST /synthesize → TTS pipeline, returns WAV audio bytes
"""

import io
import os
import sys
import logging
from flask import Flask, send_from_directory, request, jsonify, send_file

# Pipeline code is at /app/code/ (copied by Dockerfile)
_code_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "code")
if os.path.isdir(_code_dir):
    sys.path.insert(0, _code_dir)

try:
    from text_normalizer import normalize
    from synthesizer import Synthesizer, SynthConfig
    PIPELINE_AVAILABLE = True
except Exception as e:
    logging.warning(f"Pipeline import failed: {e}")
    PIPELINE_AVAILABLE = False

logging.basicConfig(level=logging.INFO)

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app = Flask(__name__, static_folder=STATIC_DIR)

# style → (words-per-minute, pitch)
STYLE_PARAMS = {
    "neutral":       (140, 50),
    "formal":        (120, 45),
    "conversational":(160, 55),
}

SPEED_MULTIPLIER = {
    "0.7x": 0.7,
    "0.85x": 0.85,
    "1x": 1.0,
    "1.15x": 1.15,
    "1.3x": 1.3,
}


# ── Static frontend ──────────────────────────────────────────────────────────

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    # Serve API routes via their own handlers (matched first by Flask routing)
    # Everything else: try to serve the file, fall back to index.html
    if path:
        file_path = os.path.join(STATIC_DIR, path)
        if os.path.isfile(file_path):
            return send_from_directory(STATIC_DIR, path)
    return send_from_directory(STATIC_DIR, "index.html")


# ── Health check ─────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    espeak_ok = (
        os.path.isfile("/usr/bin/espeak-ng") or
        os.path.isfile("/usr/local/bin/espeak-ng")
    )
    return jsonify({
        "status": "ok",
        "pipeline": PIPELINE_AVAILABLE,
        "espeak": espeak_ok,
    })


# ── TTS synthesis ─────────────────────────────────────────────────────────────

@app.route("/synthesize", methods=["POST"])
def synthesize():
    if not PIPELINE_AVAILABLE:
        return jsonify({"error": "Pipeline not available on this server"}), 503

    data = request.get_json(force=True)
    text = (data.get("text") or "").strip()
    style = data.get("style", "neutral")
    speed_label = data.get("speed", "1x")

    if not text:
        return jsonify({"error": "text is required"}), 400
    if len(text) > 3000:
        return jsonify({"error": "text must be under 3000 characters"}), 400
    if style not in STYLE_PARAMS:
        style = "neutral"

    try:
        base_rate, pitch = STYLE_PARAMS[style]
        multiplier = SPEED_MULTIPLIER.get(speed_label, 1.0)
        rate = int(base_rate * multiplier)

        # Normalize text (handles numbers, dates, abbreviations, etc.)
        normalized = normalize(text)

        # Synthesize via espeak-ng directly — bypasses prosody markup that
        # inserts _600 pause tokens which espeak-ng reads aloud as numbers
        synth = Synthesizer(SynthConfig(language="az", speed=rate, pitch=pitch))
        audio_bytes = synth.synthesize_text(normalized)

        if not audio_bytes:
            return jsonify({"error": "Synthesis produced no audio"}), 500

        return send_file(
            io.BytesIO(audio_bytes),
            mimetype="audio/wav",
            as_attachment=False,
            download_name="output.wav",
        )

    except Exception as e:
        logging.exception("Synthesis error")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
