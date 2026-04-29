"""
Flask API server for the Azerbaijani rule-based TTS pipeline.
Wraps AzTTSPipeline and returns synthesized WAV audio bytes.

Deployed on Render (free tier) as a Python web service.
espeak-ng must be installed on the server (handled in render build command).
"""

import os
import sys
import tempfile
import logging
from pathlib import Path
from flask import Flask, request, jsonify, send_file

# Add the pipeline code directory to path
CODE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../code")
sys.path.insert(0, os.path.abspath(CODE_DIR))

try:
    from pipeline import AzTTSPipeline, PipelineConfig
    PIPELINE_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Pipeline import failed: {e}")
    PIPELINE_AVAILABLE = False

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

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


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "pipeline": PIPELINE_AVAILABLE,
        "espeak": os.path.exists("/usr/bin/espeak-ng") or os.path.exists("/usr/local/bin/espeak-ng"),
    })


@app.route("/synthesize", methods=["POST"])
def synthesize():
    if not PIPELINE_AVAILABLE:
        return jsonify({"error": "Pipeline not available on this server"}), 503

    data = request.get_json(force=True)
    text = data.get("text", "").strip()
    style = data.get("style", "neutral")
    speed_label = data.get("speed", "1x")

    if not text:
        return jsonify({"error": "text is required"}), 400
    if len(text) > 3000:
        return jsonify({"error": "text must be under 3000 characters"}), 400
    if style not in STYLE_TO_RATE:
        style = "neutral"

    base_rate = STYLE_TO_RATE[style]
    multiplier = SPEED_TO_MULTIPLIER.get(speed_label, 1.0)
    rate = int(base_rate * multiplier)

    try:
        config = PipelineConfig(speaking_style=style)
        pipeline = AzTTSPipeline(config)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        output = pipeline.synthesize(text, output_path=tmp_path)
        output_path = Path(output if output else tmp_path)

        if not output_path.exists() or output_path.stat().st_size == 0:
            return jsonify({"error": "Synthesis produced no audio. Is espeak-ng installed?"}), 500

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
        try:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except Exception:
            pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
