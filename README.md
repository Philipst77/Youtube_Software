# 🎬 YouTube Auto Subtitles

A simple tool to automatically **download YouTube subtitles/transcripts** and generate `.srt` / `.vtt` caption files. It also provides an interface to quickly fetch subtitles and burn them directly into videos with FFmpeg if needed.  

This project runs locally (no external backend required) and launches a lightweight web interface at `http://localhost:5173`.

---

## ✨ Features
- 🎥 Input any YouTube video URL.  
- ⬇️ Download subtitles in **.srt** or **.vtt** format.  
- 📝 Sync subtitles with the original video timeline.  
- 🔥 Optionally burn subtitles directly into videos with `ffmpeg`.  
- 🖥️ Easy Mac launcher (`.app`) to start everything with a double-click.  

---

## 📦 Setup Instructions

### 1. Clone the Repo
git clone [https://github.com/yourusername/Youtube_Video_Downloader](https://github.com/Philipst77/Youtube_Software.git)
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

## 🔥 Burn Subtitles into Video (Optional)

If you want the transcript directly embedded into your downloaded video (hardcoded captions):

# Example with ffmpeg + .srt subtitles
ffmpeg -i "input.mp4" -vf "subtitles=subtitles.srt" -c:a copy "output_with_subs.mp4"

.vtt subtitles → convert to .srt first:

ffmpeg -i subtitles.vtt subtitles.srt

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
