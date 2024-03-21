import React from 'react';
import axios from 'axios';
import IconButton from '@mui/material/IconButton';
import MicIcon from '@mui/icons-material/Mic';
import StopIcon from '@mui/icons-material/Stop';
import { useAudioRecorder } from 'react-audio-voice-recorder';

export default function App() {
  const {
    startRecording,
    stopRecording,
    recordingBlob,
    isRecording
  } = useAudioRecorder();

  const handleStopRecording = () => {
    stopRecording();
  };

  React.useEffect(() => {
    if (recordingBlob) {
      console.log('Sending audio blob to the server', recordingBlob);
      const formData = new FormData();
      formData.append("audio", recordingBlob, "recording.webm");

      axios.post('http://localhost:5000/api/transcribe', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        console.log(response.data);
        // Handle the response from the server here
      }).catch(error => {
        console.error('Error sending audio to the server:', error);
      });
    }
  }, [recordingBlob]);

  return (
    <div>
      <IconButton
        color="primary"
        onClick={isRecording ? handleStopRecording : startRecording}
        aria-label={isRecording ? "Stop recording" : "Start recording"}
      >
        {isRecording ? <StopIcon /> : <MicIcon />}
      </IconButton>
    </div>
  );
}
