from flask import Flask, request, jsonify
from flask import send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from openai import OpenAI
from dotenv import load_dotenv
from io import BytesIO
import os

load_dotenv()


app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")
client = OpenAI()


@socketio.on("connect")
def test_connect():
    print("Client connected.")


@socketio.on("disconnect")
def test_disconnect():
    print("Client disconnected.")


@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory("static/audio", filename)


@socketio.on("audio_data")
def handle_audio(data):
    # audio_file = data["audio"]
    try:
        print(type(data))
        # Wrap the file content in a BytesIO object
        audio_bytes_io = BytesIO(data)
        print(type(audio_bytes_io))

        # Prepare the tuple (filename, file-like object, content_type)
        file_tuple = ("audio.webm", audio_bytes_io, "audio/webm")

        # Pass the tuple to the transcription API
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=file_tuple
        )

        print(f"Text: {transcription.text}")
        emit("transcription", {"text": transcription.text})

        response = get_response(transcription.text)
        emit("response", {"text": response})

        audio_filename = "new_output.mp3"
        audio_url = synthesize_audio(response, audio_filename)
        emit("audio_url", {"url": audio_url})

    except Exception as e:
        print("An error occurred: ", str(e))


def get_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    response = completion.choices[0].message.content
    print(response)

    return response


def synthesize_audio(text, audio_filename):
    audio = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    audio_url = os.path.join("static", "audio", "new_output.mp3")
    audio.stream_to_file(audio_url)
    print(type(audio), audio)

    return audio_url


if __name__ == "__main__":
    app.run(debug=True)
