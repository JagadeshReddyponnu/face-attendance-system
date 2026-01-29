# Face Authentication Attendance System

## Overview

This project is a production‑ready **Face Authentication Attendance System** built for a placement assignment. It performs real‑time face registration and recognition using a webcam, applies **liveness (spoof) prevention via natural head movement**, and marks **Punch‑In / Punch‑Out** with persistence. The system is exposed as a **FastAPI backend**, ready for frontend or mobile integration.

## Key Features

* Real‑time face registration and recognition (camera input)
* Natural head‑movement liveness detection (spoof prevention)
* Automatic **IN / OUT** attendance logic
* Minimum time‑gap enforcement between entries
* Daily reset (first entry of the day is IN)
* Persistent storage using SQLite
* Production API using FastAPI with interactive docs

## Tech Stack

* **Language:** Python 3
* **Computer Vision / ML:** OpenCV, DeepFace (FaceNet embeddings)
* **Backend:** FastAPI, Uvicorn
* **Database:** SQLite
* **Environment:** Virtualenv

## Project Structure

```
face-attendance-system/
├── app.py                 # FastAPI service
├── attendance.py          # Local attendance runner
├── camera.py              # Camera test
├── database.py            # SQLite helpers
├── face_encoder.py        # Face embedding extraction
├── matcher.py             # Embedding matching logic
├── recognize_live.py      # Live recognition (no attendance)
├── recognition.py         # Face registration
├── spoof_check.py         # Liveness (head movement)
├── attendance.db          # SQLite database
├── data/
│   └── registered_faces/  # Saved embeddings (.npy)
├── requirements.txt
└── README.md
```

## System Architecture

```
Webcam
  │
  ▼
Face Detection
  │
  ▼
Face Embedding (FaceNet)
  │
  ├──► Liveness Check (Natural Head Movement)
  │
  ▼
Embedding Matching (Distance Threshold)
  │
  ▼
Attendance Logic (IN / OUT)
  │
  ▼
SQLite Database
```

## How Attendance Works

* If no entry exists today → **IN**
* If last entry today is **IN** → **OUT**
* Enforces a minimum time gap to avoid duplicate entries
* State is persisted in SQLite

## Spoof Prevention (Liveness)

* Passive liveness detection using **natural head movement across frames**
* Blocks static images and screen replays
* Lightweight, user‑friendly, and suitable for low‑quality webcams

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run Locally (Script Mode)

### Register a Face

```bash
python recognition.py
```

### Live Recognition

```bash
python recognize_live.py
```

### Attendance System

```bash
python attendance.py
```

## Run as API (Production)

```bash
uvicorn app:app --reload
```

* Root: `http://127.0.0.1:8000`
* Swagger UI: `http://127.0.0.1:8000/docs`
* Attendance Endpoint: `POST /attendance`

## Accuracy Expectations

* Good lighting: ~90–95% recognition accuracy
* Low lighting or occlusion may reduce accuracy
* Liveness blocks basic spoofing (photos/screens), not advanced deepfakes

## Known Limitations

* Sensitive to very poor lighting
* Advanced spoof attacks are out of scope
* Single‑camera, single‑process usage

## Interview Talking Points

* Separation of ML (embeddings) and deterministic logic (attendance)
* Liveness implemented as passive head‑movement detection
* Transition from scripts to a production API using FastAPI
* Honest discussion of ML limitations and tradeoffs

## Submission Notes

* Works with real camera input
* Includes spoof prevention
* Clean, modular codebase
* Ready for frontend or mobile integration
