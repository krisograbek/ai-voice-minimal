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

            get_response(transcription.text)

            return jsonify({"text": transcription.text}), 200

        except Exception as e:
            print("An error occurred: ", str(e))
            return jsonify({"error": "An error occurred during transcription"}), 500
    else:
        return jsonify({"error": "No audio file found in request"}), 400


@app.route("/api/respond", methods=["POST"])
def get_response(prompt):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    response = completion.choices[0].message.content
    print(response)

    synthesize_audio(response)

    return jsonify({"response": response}), 200


@app.route("/api/synthesize", methods=["POST"])
def synthesize_audio(text):
    client = OpenAI()

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    response.stream_to_file("./audio/output.mp3")

    return jsonify({"audio_url": "URL to the synthesized audio"}), 200


if __name__ == "__main__":
    app.run(debug=True)
