# FaceMatch Pro — Face comparison GUI

FaceMatch Pro is a desktop application (Python + Tkinter) to compare two photos and estimate whether they belong to the same person using face embeddings via the `face_recognition` library.  
It provides a tolerance slider (match threshold), face detection visualization (bounding boxes), a distance/similarity readout, and a comparison history with export options. 

## Motivation

This project was created after a friend working on customer identity verification (banking sector) had to repeatedly verify multiple photos of the same user as part of a KYC / identity verification workflow. 
The goal is to speed up manual checks with a simple UI that shows an interpretable score (distance + derived similarity), a configurable threshold, and a history log. 

## Disclaimer (important)

- This tool is for educational and assistance purposes only; it is not a compliant identity verification solution. 
- Face recognition can produce false positives/negatives and performance varies across lighting, pose, occlusions, and demographics. 
- Do not use this project to process or publish sensitive personal data without proper authorization and legal basis. 

## Features

- GUI to load two images (JPG/JPEG/PNG) using file dialogs. 
- Face detection and drawing bounding boxes on each loaded image. 
- Configurable tolerance slider (default tolerance is 0.5). 
- Face comparison using face distance and a derived similarity percentage:
  - distance = `face_recognition.face_distance(...)` 
  - similarity = `(1 - distance) * 100` 
- Visual feedback:
  - Progress bar during processing. 
  - Chart comparing “Distance” vs “Tolerance”. 
- History of comparisons (date, filenames, distance, result) with a table viewer. 
- Export history to CSV. 
- Save results to a TXT report. 

## Tech stack

- Python (application logic). 
- Tkinter + ttk (GUI). 
- face_recognition (face detection/encodings and distance). 
- OpenCV (drawing rectangles). 
- Pillow (image loading/display). 
- Matplotlib (embedded chart in Tkinter). 
- NumPy (image arrays). 

## Getting started

### Requirements

- Python 3.x. 
- System dependencies: `face_recognition` typically requires dlib wheels/compiled dependencies depending on OS. 

### Installation

Clone the repo:
```bash
git clone https://github.com/<your-user>/<your-repo>.git
cd <your-repo>
