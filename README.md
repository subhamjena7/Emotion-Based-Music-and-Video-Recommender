# Emotion-Based Music and Video Recommender System

## Overview

The primary purpose of this project is to develop an advanced music and video recommender system that takes into account the user’s emotional state. By aligning suggestions with the user’s current emotions, the system aims to enhance the overall listening and viewing experience. Whether a user is feeling happy, sad, or angry, the system will tailor its recommendations accordingly.

## Features

- **Emotion Detection**: Capture real-time video feed from a webcam or use static images to detect faces using OpenCV. This involves using a pre-trained model like `haarcascade_frontalface_default.xml` for face detection.
- **Emotion Prediction**: Once faces are detected, the next step is to predict the emotion of the person. This is where the `fer.h5` file comes into play. It’s a pre-trained deep learning model, likely trained on the FER2013 dataset, which can classify emotions into categories such as happy, sad, angry, etc.
- **Music and Video Recommendation**: Based on the detected emotion, the system then recommends music. This could be done by fetching playlists from a music service like Spotify and YouTube that match the mood associated with the recognized emotion.
- **Web Application**: All these components are integrated into a web application, using a framework like Flask, which allows users to interact with the system in real-time.

## Keywords

1. **OpenCV2**
2. **FER dataset**
3. **fer.h5 (Deep Learning Model)**
4. **Flask**
5. **YouTube**
6. **Spotify**

## Usage

1. **Access the web application**:
    Open your browser and go to `http://127.0.0.1:5000/`.

2. **Interact with the system**:
    - Allow the application to access your webcam or upload a static image.
    - The system will detect faces and predict the emotion.
    - Based on the emotion, the system will fetch and display music and video recommendations from Spotify and YouTube.

## Acknowledgments

- The FER2013 dataset for providing the necessary data for training the emotion detection model.
- OpenCV for the face detection model.
- Spotify and YouTube for their music and video services.
