import React from 'react';
import { AudioRecorder } from 'react-audio-voice-recorder';
import axios from 'axios';

export default function App() {
  const handleRecordingComplete = (blob) => {
    // Create an audio URL for playback (if needed)
    const url = URL.createObjectURL(blob);
    const audio = document.createElement('audio');
    audio.src = url;
    audio.controls = true;
    document.body.appendChild(audio);
    console.log(blob)

    // Create a FormData object to hold the audio blob
    const formData = new FormData();
    formData.append('audio', blob, 'recording.webm');

    // Send the audio blob to the backend
    axios.post('http://localhost:5000/api/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
      .then(response => {
        console.log('Transcription:', response.data);
        // You can handle further steps here or chain .then() calls
      })
      .catch(error => {
        console.error('Error sending audio to backend:', error);
      });
  };

  return (
    <div>
      <AudioRecorder
        onRecordingComplete={handleRecordingComplete}
        audioTrackConstraints={{
          noiseSuppression: true,
          echoCancellation: true,
          // additional constraints can be added here if needed
        }}
        onNotAllowedOrFound={(err) => console.table(err)}
        // downloadOnSavePress={true}
        downloadFileExtension="webm"
        mediaRecorderOptions={{
          audioBitsPerSecond: 128000,
        }}
      // Uncomment if you want to show the visualizer
      // showVisualizer={true}
      />
      <br />
    </div>
  );
}
