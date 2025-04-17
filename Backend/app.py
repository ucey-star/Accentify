from flask import Flask, request
from flask_cors import CORS  # Import CORS
from scripts.train import extract_features  # Assuming 'model' is your trained model variable
import subprocess  # Import subprocess
import pickle 
import logging

# Assuming you have a mapping function or dictionary from label encodings back to accent names
# If this mapping is part of your training script, import it as well
# If not, you'll need to create it based on your LabelEncoder from the training script
#from scripts.train import label_to_accent_mapping

# Set up basic logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)  # Enable CORS on the app

# Load the model, LabelEncoder, and StandardScaler from disk
with open('trained_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('label_encoder.pkl', 'rb') as file:
    le = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)


@app.route('/analyze', methods=['POST'])
def analyze():
    # Check if an audio file was uploaded
    if 'audioFile' not in request.files:
        return {"error": "Missing audio file"}, 400

    # Get the audio file from the POST request
    audio_file = request.files['audioFile']
    logging.info(f"Received audio file for processing: {audio_file.filename}")
    [print("audio file", audio_file)]
    print("request files", request.files)

    # Save the audio file temporarily to process
    temp_audio_path = 'temp_audio.webm'  # Instead of 'temp_audio.wav'
    audio_file.save(temp_audio_path)

    output_audio_path = 'converted_audio.wav'  # Output file
    ffmpeg_command = ['ffmpeg', '-i', temp_audio_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '22050', '-ac', '2', output_audio_path]
    try:
        subprocess.run(ffmpeg_command, check=True)  # Run FFmpeg command
    except subprocess.CalledProcessError as e:
        return {"error": f"Failed to convert audio: {e}"}, 500

    # Process the audio file to extract features
    features = extract_features(output_audio_path) 
    if features is None:
        logging.error("Error processing the audio file.")
        return {"error": "Error processing the audio file"}, 500

    # Reshape features for prediction if necessary (depends on your model input)
    features_scaled = scaler.transform(features.reshape(1, -1))

    # Predict the accent using the pre-trained model
    predicted_accent_index = model.predict(features_scaled)[0]
    predicted_accent = le.inverse_transform([predicted_accent_index])[0]  # Convert label index back to accent name

    # Return the predicted accent
    return {"accent": predicted_accent}

if __name__ == '__main__':
    app.run(debug=True)
