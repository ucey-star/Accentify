import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [audioURL, setAudioURL] = useState(''); // Store the audio URL
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [detectedAccent, setDetectedAccent] = useState(''); // Store the detected accent


  useEffect(() => {
    // Request Microphone access
    navigator.mediaDevices.getUserMedia({ audio: true })
      .then(stream => {
        const options = { mimeType: 'audio/webm' };  // WebM format
        const newMediaRecorder = new MediaRecorder(stream, options);
        setMediaRecorder(newMediaRecorder);

        newMediaRecorder.ondataavailable = async e => {
          const audioBlob = new Blob([e.data], { 'type': 'audio/webm' });
          const newAudioURL = URL.createObjectURL(audioBlob); // Create a URL for the blob
          setAudioURL(newAudioURL); // Update the component state with the new URL

          const formData = new FormData();
          formData.append('audioFile', audioBlob, 'user_audio.wav');

          // Send audio file directly to the server
          fetch('http://127.0.0.1:5000/analyze', { method: 'POST', body: formData })
            .then(response => response.json())
            .then(data => {
              console.log(data);
              setDetectedAccent(data.accent); // Update the state with the detected accent
            })
            .catch(error => console.error('Error:', error))
        };
      });
  }, []);

  const startRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.start();
      setIsRecording(true);
      setAudioURL(''); // Clear the previous recording
    }
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h2>Accentify</h2>
        {isRecording ? (
          <button className="button" onClick={stopRecording}>Stop Recording</button>
        ) : (
          <button className="button" onClick={startRecording}>Start Recording</button>
        )}
        {audioURL && <audio src={audioURL} controls="controls" />} {/* Display the audio player if there is a recording */}
        {detectedAccent && <p>Your detected accent: {detectedAccent}</p>}
      </header>
    </div>
  );
}

export default App;
