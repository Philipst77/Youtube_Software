# 🎬 YouTube Auto Subtitles

A lightweight tool to generate, preview, and download subtitles for YouTube videos and local media files. It automatically creates `.srt` and `.vtt` caption files, previews subtitles in sync with video playback, and optionally burns subtitles directly into videos using FFmpeg.

The app runs **100% locally** and launches a web interface at:  
👉 **http://localhost:5173**

---

## ✨ Features

- 🎥 Paste any YouTube video URL
- 📁 Upload local video/audio files (`.mp4`, `.mov`, `.mkv`, `.mp3`, `.wav`)
- 🧠 Automatic transcription using Whisper
- 🌍 Optional subtitle translation
- ⬇️ Download subtitles as `.srt` or `.vtt`
- ▶️ Live subtitle preview synced to video playback
- 🔥 Optional hard-burned subtitles with FFmpeg
- 🐳 Dockerized — no local Python / Node / FFmpeg setup required

---

## 🚀 Recommended: Run with Docker (One Command)

This is the **preferred and easiest** way to run the app.

### Requirements
- Docker Desktop (Mac / Windows / Linux)

### Run
```bash
docker compose up
```

Then open:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5001

That's it. **No Python. No Node. No FFmpeg installs.**

---

## 📦 What Docker Does for You

- Packages Python, Node, FFmpeg, Whisper, dependencies
- Uses prebuilt images from Docker Hub
- Caches Whisper models to avoid re-downloads
- Works identically on all operating systems

---

## ⬇️ Downloadable Files

After transcription, you can download:

✅ `.srt` subtitle files (for video editors & players)  
✅ `.vtt` subtitle files (for web players)

Downloads are available directly from the web UI.

---

## 🔥 Burn Subtitles into Video (Optional)

To permanently embed subtitles into a video:
```bash
# Convert .vtt → .srt (if needed)
ffmpeg -i subtitles.vtt subtitles.srt

# Burn subtitles into the video
ffmpeg -i input.mp4 -vf "subtitles=subtitles.srt" -c:a copy output_with_subs.mp4
```

This creates a video with hardcoded captions.

---

## 🧪 Manual Setup (Optional / Development Only)

⚠️ **Not recommended** unless you are developing the app

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

Open: 👉 **http://localhost:5173**

---

## 📂 Project Structure
```
Youtube_Video_Transcriber/
│── backend/            # Flask API + Whisper transcription
│── frontend/           # Vite / React web UI
│── docker-compose.yml
│── README.md
```

---

## 🛠️ Tech Stack

- **yt-dlp** – YouTube audio extraction
- **faster-whisper** – Fast, local transcription
- **FFmpeg** – Audio extraction & subtitle burning
- **Flask** – Backend API
- **React + Vite** – Frontend UI
- **Docker & Docker Compose** – Packaging & distribution

---

## ⚡ Example Workflow

1. Paste a YouTube link or upload a video
2. Click **Generate**
3. Preview subtitles synced with the video
4. Download `.srt` / `.vtt`
5. (Optional) Burn subtitles into the video

**Done** ✅

---

## 📌 Notes

- All processing happens **locally**
- No data is uploaded to external servers
- Docker is the **recommended** way to run the app
- Works on macOS, Windows, and Linux

---

## 🐳 Docker Images

Prebuilt images are available on Docker Hub:

- `philipst77/youtube_software:backend`
- `philipst77/youtube_software:frontend`

Used automatically by `docker-compose.yml`.
