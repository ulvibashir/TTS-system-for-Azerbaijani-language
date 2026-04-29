"""
Single-service server for the Azerbaijani rule-based TTS demo.

Serves:
  GET  /          → Next.js static frontend (built into /app/static/)
  GET  /health    → JSON health check
  POST /synthesize → TTS pipeline, returns WAV audio bytes
"""

import os
import sys
import tempfile
import logging
from pathlib import Path
from flask import Flask, send_from_directory, request, jsonify, send_file

# Pipeline code is at /app/code/ (copied by Dockerfile)
_code_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "code")
if os.path.isdir(_code_dir):
    sys.path.insert(0, _code_dir)

try:
    from pipeline import AzTTSPipeline, PipelineConfig
    PIPELINE_AVAILABLE = True
except Exception as e:
    logging.warning(f"Pipeline import failed: {e}")
    PIPELINE_AVAILABLE = False

logging.basicConfig(level=logging.INFO)

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app = Flask(__name__, static_folder=STATIC_DIR)

STYLE_TO_RATE = {
    "neutral": 140,
    "formal": 120,
    "conversational": 160,
}

SPEED_TO_MULTIPLIER = {
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
    if style not in STYLE_TO_RATE:
        style = "neutral"

    tmp_path = None
    try:
        config = PipelineConfig(speaking_style=style)
        pipeline = AzTTSPipeline(config)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        output = pipeline.synthesize(text, output_path=tmp_path)
        output_path = Path(output if output else tmp_path)

        if not output_path.exists() or output_path.stat().st_size == 0:
            return jsonify({"error": "Synthesis produced no audio"}), 500

        return send_file(
            str(output_path),
            mimetype="audio/wav",
            as_attachment=False,
            download_name="output.wav",
        )

    except Exception as e:
        logging.exception("Synthesis error")
        return jsonify({"error": str(e)}), 500

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception:
                pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
