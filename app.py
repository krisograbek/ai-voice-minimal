import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()


client = OpenAI()


app = Flask(__name__)
CORS(app)


@app.route("/api/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" in request.files:
        audio_file = request.files["audio"]
        try:
            # Wrap the file content in a BytesIO object
            audio_bytes_io = BytesIO(audio_file.read())

            # Prepare the tuple (filename, file-like object, content_type)
            file_tuple = ("audio.webm", audio_bytes_io, "audio/webm")

            # Pass the tuple to the transcription API
            transcription = client.audio.transcriptions.create(
                model="whisper-1", file=file_tuple
            )

            print(f"Text: {transcription.text}")

            # Assuming the response is a JSON string, parse it into a dictionary
            # transcription_dict = json.loads(transcription)
            # Access the transcription result
            return jsonify({"text": transcription.text}), 200

        except Exception as e:
            print("An error occurred: ", str(e))
            return jsonify({"error": "An error occurred during transcription"}), 500
    else:
        return jsonify({"error": "No audio file found in request"}), 400


@app.route("/api/respond", methods=["POST"])
def get_response():
    # This is where you'll send the transcribed text to GPT-4 and get a response.
    # Placeholder for GPT-4 interaction logic.
    return jsonify({"response": "GPT-4 response here"}), 200


@app.route("/api/synthesize", methods=["POST"])
def synthesize_audio():
    # This is where you'll convert the GPT-4 text response to audio using TTS.
    # Placeholder for TTS conversion logic.
    return jsonify({"audio_url": "URL to the synthesized audio"}), 200


if __name__ == "__main__":
    app.run(debug=True)
