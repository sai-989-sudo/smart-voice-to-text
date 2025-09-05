from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from sst import transcribe_audio
from nlp_pipeline import extract_insights

app = Flask(__name__)
CORS(app)

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    file_path = "temp.wav"
    audio_file.save(file_path)

    try:
        transcript = transcribe_audio(file_path)
        insights = extract_insights(transcript)

        return jsonify({
            "transcript": transcript,
            "insights": insights
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    app.run(debug=True)
