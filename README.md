# Neural Speech-to-Text Platform

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/container-Docker-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


A containerized automatic speech recognition (ASR) platform implementing end-to-end neural transcription using OpenAI’s Whisper model. The system processes YouTube URLs and local media files, generates synchronized subtitle outputs, and provides optional hard-coded subtitle rendering through FFmpeg.

---

## Overview

This project implements a fully self-hosted speech-to-text inference pipeline designed for local deployment. It combines neural transcription, media preprocessing, subtitle generation, and frontend visualization within a reproducible containerized architecture.

The system extracts audio from YouTube videos or uploaded media, performs high-accuracy transcription using Whisper, generates synchronized `.srt` and `.vtt` subtitle files, and supports optional subtitle translation and permanent subtitle embedding.

The architecture separates backend inference logic from frontend presentation, enabling modular deployment and consistent cross-platform execution through Docker.

---

## Core Capabilities

### 1. Neural Transcription

- Transformer-based speech-to-text inference using Whisper
- Support for multilingual transcription and translation
- Local inference without external API dependencies

### 2. Media Processing

- YouTube audio extraction via `yt-dlp`
- Audio decoding and preprocessing via FFmpeg
- Subtitle synchronization in `.srt` and `.vtt` formats
- Optional hard-burned subtitle rendering

### 3. Web Interface

- Local frontend served at `http://localhost:5173`
- Real-time subtitle preview synchronized to playback
- Direct subtitle file download from the UI

### 4. Containerized Deployment

- Fully reproducible Docker environment
- Backend and frontend services orchestrated via Docker Compose
- No local Python, Node, or FFmpeg installation required

---

## Architecture

The platform is structured as a two-service system:

    Youtube_Software/
    │
    ├── backend/            # Flask API + Whisper inference
    ├── frontend/           # React + Vite interface
    ├── docker-compose.yml  # Service orchestration
    └── README.md

- **Backend**: Handles audio extraction, transcription, subtitle generation, and media processing  
- **Frontend**: Provides a responsive interface for file upload, URL submission, and subtitle preview  
- **Docker Layer**: Encapsulates runtime dependencies and ensures platform consistency  

---

## Deployment (Recommended)

### Requirements

- Docker Desktop (macOS, Windows, or Linux)

### Run

```bash
curl -O https://raw.githubusercontent.com/Philipst77/Youtube_Software/master/docker-compose.yml && docker compose up

```

Access:

- Frontend: http://localhost:5173  
- Backend API: http://localhost:5001  

The system runs entirely locally within Docker containers.

---
---
#  Permanent Subtitle Embedding (Hard Burn)

You can permanently embed subtitles into an `.mp4` video using FFmpeg. Hard-burned subtitles become part of the video frames and cannot be disabled.

## If You Have an `.srt` File
```bash
ffmpeg -i input.mp4 -vf "subtitles=subtitles.srt" -c:a copy output_subtitled.mp4
```

## If You Have a `.vtt` File
```bash
ffmpeg -i input.mp4 -vf "subtitles=subtitles.vtt" -c:a copy output_subtitled.mp4
```

## If Encoding Issues Occur (Convert `.vtt` → `.srt` First)
```bash
ffmpeg -i subtitles.vtt subtitles.srt
ffmpeg -i input.mp4 -vf "subtitles=subtitles.srt" -c:a copy output_subtitled.mp4
```

##  Command Breakdown

- `-i input.mp4` → Input video file
- `-vf "subtitles=..."` → Applies subtitle video filter
- `-c:a copy` → Copies original audio without re-encoding
- `output_subtitled.mp4` → Final video with embedded subtitles
---
## Manual Development Setup (Optional)

### Requirements

- Python 3.11+
- Node.js
- FFmpeg

### Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
npm install
npm run dev
```

---

## Technology Stack

- Whisper (Transformer-based ASR)
- faster-whisper (optimized inference)
- yt-dlp (media extraction)
- FFmpeg (audio decoding and subtitle rendering)
- Flask (backend API)
- React + Vite (frontend interface)
- Docker & Docker Compose (containerization)

---

## Design Principles

- Fully local, privacy-preserving inference  
- Clear separation between inference backend and UI layer  
- Reproducible containerized deployment  
- Modular architecture for future ASR experimentation  
- Cross-platform consistency via Docker  

---

## Usage Workflow

1. Submit a YouTube URL or upload a local media file  
2. Perform neural transcription  
3. Preview synchronized subtitles  
4. Download `.srt` or `.vtt` files  
5. Optionally render subtitles directly into the video  

---

## Notes

- All processing occurs locally  
- No external API calls are required  
- Compatible with macOS, Windows, and Linux  
- Prebuilt Docker images available via Docker Hub  
