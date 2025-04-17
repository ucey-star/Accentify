# 🗣️ Accentify – Real-Time Accent Detection with Voice Input

**Accentify** is a full-stack AI-powered web application that detects English accents in real time from recorded voice input. It uses a Flask backend with a trained ML model and a React frontend to record, send, and display the predicted accent.

---

## 🎯 Features

- 🎤 **Live Voice Recording** (WebM format using MediaRecorder API)  
- 🔁 **Real-Time Prediction** using a pre-trained model  
- 🧠 **ML-Powered Accent Classification** (e.g., Nigerian, British, American)  
- 🌐 **Flask REST API** for processing and returning predictions  
- 🎛️ **Automatic Audio Conversion** (WebM → WAV using FFmpeg)  
- ⚛️ **React Frontend** with one-click record & playback interface  

---

## 🛠️ Tech Stack

### 🧩 Backend (Python + Flask)
- Flask + Flask-CORS  
- Pretrained ML model (scikit-learn)  
- LabelEncoder + Scaler  
- FFmpeg via subprocess for audio conversion  

### 🎧 Frontend (React.js)
- MediaRecorder API for capturing audio  
- `fetch` API to send audio as `FormData`  
- Dynamic UI updates with predicted accent  

---

## 📁 Project Structure

```
Accentify/
├── scripts/
│   ├── train.py                # Model training and feature extraction
│   ├── app.py                  # Flask API backend
│   ├── scaler.pkl              # Scaler used during training
│   ├── label_encoder.pkl       # Label encoder for class names
│   ├── trained_model.pkl       # Final ML model
├── Frontend/
│   └── src/
│       ├── App.js              # React logic
│       ├── App.css            # Styles
│       └── index.js, etc.
├── temp_audio.webm / converted_audio.wav (runtime)
```

---

## 🚀 How to Run

### 🧠 Backend (Flask API)
1. Install dependencies:
   ```bash
   pip install flask flask-cors numpy scikit-learn
   ```
2. Make sure you have [FFmpeg](https://ffmpeg.org/download.html) installed and available in your system path.
3. Run the server:
   ```bash
   python scripts/app.py
   ```
   > The server will be available at `http://127.0.0.1:5000`

---

### 🎛️ Frontend (React)
1. Navigate to the `Frontend/` directory:
   ```bash
   cd Frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the app:
   ```bash
   npm start
   ```
   > Opens on `http://localhost:3000`

---

## 🔄 How It Works

1. User clicks **Start Recording**.
2. Audio is captured in **WebM** format via the browser.
3. The recorded file is sent to the **Flask API** via `FormData`.
4. The API:
   - Converts WebM → WAV using `ffmpeg`
   - Extracts audio features
   - Applies the scaler + model to predict the accent
   - Returns the accent label
5. The UI displays the **detected accent**.

---

## 🧪 Example Output

```
Your detected accent: British
```

---

## 📦 Model Training (Optional)

You can train your own model using `scripts/train.py`, which:
- Extracts features (MFCC, etc.)
- Trains a classifier
- Saves the model, scaler, and label encoder

---

## 💡 Future Improvements

- 🎙️ Add support for longer or live-streamed audio
- 📊 Show model confidence or multiple accent probabilities
- 🧑‍🎤 Fine-tune models with larger multilingual datasets
- ☁️ Deploy to cloud (Render, Heroku, Vercel, etc.)

---

## 📄 License

This project is for educational and research purposes only.

