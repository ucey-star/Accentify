import os
import pandas as pd
import numpy as np
from pydub import AudioSegment
from python_speech_features import mfcc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from collections import Counter
import pickle

# Path to the dataset
#dataset_path = 'cv-corpus-17.0-delta-2024-03-15/en'
dataset_path = '../../Downloads/en'
tsv_file_path = os.path.join(dataset_path, 'validated.tsv')
clips_dir_path = os.path.join(dataset_path, 'clips')

# Read the metadata
df = pd.read_csv(tsv_file_path, sep='\t').sample(frac=0.1, random_state=42)

# Function to convert mp3 file to wav format
def mp3_to_wav(audio_file_path):
    audio = AudioSegment.from_mp3(audio_file_path)
    audio = audio.set_channels(1)  # Ensure mono sound
    audio = audio.set_frame_rate(22050)  # Set frame rate
    return np.array(audio.get_array_of_samples())

# Function to extract features from an audio file
def extract_features(file_path, min_duration=0.1):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        print(f"File {file_path} does not exist or is empty")
        return None
    try:
        wav_data = mp3_to_wav(file_path)
        sample_rate = 22050
        if len(wav_data) < min_duration * sample_rate:
            print(f"File {file_path} is too short for processing")
            return None
        mfccs = mfcc(wav_data, samplerate=sample_rate, numcep=40)
        mfccs_processed = np.mean(mfccs, axis=0)
    except Exception as e:
        print(f"Error encountered while parsing file: {file_path}, Error: {e}")
        return None
    return mfccs_processed

features = []
labels = []

for index, row in df.iterrows():
    file_path = os.path.join(clips_dir_path, str(row['path']))
    class_label = row['accent']
    data = extract_features(file_path)
    if data is not None:
        features.append(data)
        labels.append(class_label)

if len(features) > 1 and len(labels) > 1:
    features = np.array(features)
    labels = np.array(labels)
    le = LabelEncoder()
    labels_encoded = le.fit_transform(labels)
    label_to_accent_mapping = {index: label for index, label in enumerate(le.classes_)}
    X_train, X_test, y_train, y_test = train_test_split(features, labels_encoded, test_size=0.2, random_state=42)

    # Optionally apply standard scaling to features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f'Accuracy: {accuracy * 100:.2f}%')

    # Save the trained model to disk
    with open('trained_model.pkl', 'wb') as file:
        pickle.dump(model, file)

    # Optionally, save LabelEncoder and StandardScaler if you'll need them for preprocessing in prediction
    with open('label_encoder.pkl', 'wb') as file:
        pickle.dump(le, file)

    with open('scaler.pkl', 'wb') as file:
        pickle.dump(scaler, file)

# Print class distribution after labels are populated
class_distribution = Counter(labels)
print("Class distribution:", class_distribution)
