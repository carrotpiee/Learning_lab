# AI Liveness Detection System

## Problem Statement
Traditional face authentication systems can be fooled using photos, videos, or screen replays.

## Solution
This project is a real-time AI-based liveness detection system built using Python, OpenCV, and MediaPipe.

It verifies whether the detected face belongs to a live person by performing challenge-response verification.

## Features
- Real-time webcam face detection
- Blink detection
- Head movement tracking
- Live person verification
- Spoof detection

## Technologies Used
- Python
- OpenCV
- MediaPipe

## How It Works
1. Detect face
2. Ask user to blink
3. Ask user to turn head left
4. Ask user to turn head right
5. Verify liveness

## Installation
Install dependencies:

pip install opencv-python mediapipe

## Run
python main.py

## Team Objective
To build a simple, free, real-time liveness detection prototype for anti-spoof facial authentication.

## Future Improvements
- Voice challenge verification
- Anti-video replay detection
- Mobile app deployment
- Deep learning-based spoof classification