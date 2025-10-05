# 🎬 YouTube Auto Subtitles (🚀 GPU-Accelerated Edition)

A simple tool to automatically **download and transcribe YouTube videos** using **GPU acceleration** for ultra-fast performance.  
This version leverages **PyTorch CUDA + Faster-Whisper** to process audio and subtitles directly on your GPU (falling back to CPU if no GPU is available).  

It also provides an interface to quickly fetch subtitles, translate them, and optionally burn them into the video using `ffmpeg`.  
The backend is built with **Flask** and the frontend with **Vite (React)** — everything runs **locally** on your computer.

---

## ⚙️ Highlights
- ⚡ **GPU-accelerated** transcription (via PyTorch + CUDA + Faster-Whisper)
- 🎥 Input any YouTube video URL
- ⬇️ Download subtitles in `.srt` or `.vtt` format
- 🌍 Automatic translation into any target language
- 🔥 Optionally burn subtitles into the video with `ffmpeg`
- 🚪 **Automatic port management** (if 5001 or 5173 are busy, the next available port is used)
- 🖥️ One-click launchers:
  - 🍎 **Easy macOS Launcher (.app)** via Automator  
  - 🪟 **Easy Windows Launcher (.bat / .sh)** for WSL-based startup  

This project runs entirely **offline** — no external servers or API keys required.  
Once started, access the app at [http://localhost:5173](http://localhost:5173).

---


## 📦 Setup Instructions

### 1. Clone the Repo
git clone https://github.com/Philipst77/Youtube_Software.git
cd Youtube_Video_Downloader

### 2. Install Dependencies
Use Python + Node.js (depending on your implementation):

# Python (transcription / subtitle handling)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Frontend (local web app)
npm install

### 3. Start the App
Run manually in two steps:

source .venv/bin/activate
npm run dev

Then open:  
👉 http://localhost:5173

---

## 🚀 macOS Launcher (Optional)

Instead of running commands every time, you can create a clickable app with Automator:

1. Open Automator → New Document → Application.  
2. Add action: Run Shell Script.  
3. Paste this your shell Script then save.



4. Save as `YouTubeSubtitles.app` (e.g., Desktop).  
5. ✅ Now double-clicking the `.app` launches the server and opens the web interface automatically.  

---

## 🪟 Windows Launcher (Optional)

Instead of typing commands or opening WSL manually every time, you can make a **one-click desktop launcher** to start your app automatically.  

### 1️⃣ Create a run_all.sh file (WSL/Linux script)

In your project root (e.g., Video_Transcriber/run_all.sh):

#!/bin/bash
# Kill any previous processes
fuser -k 5001/tcp 2>/dev/null
fuser -k 5173/tcp 2>/dev/null

echo "🚀 Starting Flask backend..."
cd "$(dirname "$0")/Youtube_Software/backend"
source .venv/bin/activate
python3 app.py &
BACKEND_PID=$!

echo "🌐 Starting Vite frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

sleep 5

# Automatically open the app in your browser
if command -v wslview &> /dev/null; then
  wslview "http://localhost:5173"
elif command -v xdg-open &> /dev/null; then
  xdg-open "http://localhost:5173"
elif command -v open &> /dev/null; then
  open "http://localhost:5173"
else
  echo "🌐 Please open http://localhost:5173 manually"
fi

echo ""
echo "✅ Both backend and frontend are running!"
echo "Backend: http://127.0.0.1:5001"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both."

wait $BACKEND_PID $FRONTEND_PID

Then make it executable:
chmod +x run_all.sh


### 2️⃣ Create a run_all.bat file (Windows script)

Place this file in the same directory as your run_all.sh:

@echo off
cd /d "%~dp0"
wsl bash -c "./run_all.sh"
pause


### 3️⃣ Create a Desktop Shortcut

1. Right-click run_all.bat → Send to → Desktop (create shortcut)
2. Rename it (e.g., 🧠 Launch Video Transcriber)
3. Double-click it anytime to:
   - ✅ Start Flask backend (GPU-enabled)
   - ⚙️ Start Vite frontend
   - 🌐 Open http://localhost:5173 in your browser


### 💡 Notes

- Make sure Node.js and npm are installed on Windows or WSL.
- You can stop the app anytime with Ctrl + C.
- The script automatically clears ports 5001 and 5173 before launch to avoid conflicts.


## 🔥 Burn Subtitles into Video (Optional)

If you want the transcript directly embedded into your downloaded video (hardcoded captions):

# Example with ffmpeg + .srt subtitles
Frist: .vtt subtitles → convert to .srt 

ffmpeg -i subtitles.vtt subtitles.srt


ffmpeg -i "input.mp4" -vf "subtitles=subtitles.srt" -c:a copy "output_with_subs.mp4"


---

## 📂 Project Structure

Youtube_Video_Downloader/  
│── backend/           # Subtitle fetch + transcription (Python/yt-dlp/faster-whisper)  
│── frontend/          # Web UI (npm dev server)  
│── subtitles/         # Saved .srt / .vtt files  
│── requirements.txt   # Python dependencies  
│── package.json       # Node.js dependencies  
│── launch_subtitles.sh # Optional shell launcher  

---

## 🛠️ Tech Stack
- yt-dlp – YouTube video & subtitle extraction  
- faster-whisper – Fast subtitle transcription  
- FFmpeg – Burn subtitles into video  
- Flask (backend) + Vite/React (frontend)  
- Automator / shell scripts for macOS integration  

---

## ⚡ Example Workflow
1. Paste a YouTube link → click Generate.  
2. Download subtitles as `.srt` or `.vtt`.  
3. (Optional) Burn them into your video with FFmpeg.  
4. Done ✅ — you now have a synced transcripted video.  

---

## 📌 Notes
- This runs locally only — no data leaves your machine.  
- You must have Node.js, Python 3.11+, and FFmpeg installed.  
- macOS users can double-click the Automator `.app` for a one-click experience.  
