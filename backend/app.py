import os
import traceback
import tempfile
import shutil
import subprocess
from flask import Flask, request, jsonify
from faster_whisper import WhisperModel
import yt_dlp
from deep_translator import GoogleTranslator

# ------------------------------------------------------------
# Flask + limits
# ------------------------------------------------------------
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024 * 1024  # 2GB max upload

# ------------------------------------------------------------
# Whisper config
# ------------------------------------------------------------
# Model choice: "small", "medium", "large-v3" (bigger = slower, more accurate)
MODEL_SIZE = os.getenv("WHISPER_MODEL", "small")
COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")  # e.g., float16 on GPU
model = WhisperModel(MODEL_SIZE, compute_type=COMPUTE_TYPE)

# ------------------------------------------------------------
# File type safety
# ------------------------------------------------------------
ALLOWED_EXTS = {".mp4", ".mov", ".mkv", ".mp3", ".wav", ".m4a", ".webm"}


def allowed_file(filename: str) -> bool:
    return os.path.splitext(filename.lower())[1] in ALLOWED_EXTS


# ------------------------------------------------------------
# Caption builders
# ------------------------------------------------------------
def to_srt(segments):
    def ts(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        ms = int((t - int(t)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    lines = []
    for i, s in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{ts(s['start'])} --> {ts(s['end'])}")
        lines.append(s["text"].strip())
        lines.append("")
    return "\n".join(lines)


def to_vtt(segments):
    def ts(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = int(t % 60)
        ms = int((t - int(t)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

    lines = ["WEBVTT", ""]
    for s in segments:
        lines.append(f"{ts(s['start'])} --> {ts(s['end'])}")
        lines.append(s["text"].strip())
        lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------
# Media helpers
# ------------------------------------------------------------
def download_audio(youtube_url: str, out_dir: str) -> str:
    """Download audio track and return the filepath to an MP3."""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(out_dir, "%(id)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "noplaylist": True,
        "quiet": False,

    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        basename = f"{info['id']}.mp3"
        path = os.path.join(out_dir, basename)
        if not os.path.exists(path):
            raise FileNotFoundError("Audio not found after download.")
        return path


def extract_audio_from_file(input_path: str, out_dir: str) -> str:
    """
    Convert uploaded video/audio file to WAV for Whisper (mono, 16kHz).
    """
    output_path = os.path.join(out_dir, "audio.wav")

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-ac",
        "1",
        "-ar",
        "16000",
        output_path,
    ]

    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    if result.returncode != 0 or not os.path.exists(output_path):
        raise RuntimeError(f"FFmpeg audio extraction failed: {result.stderr}")

    return output_path


def maybe_translate(text: str, target_lang: str) -> str:
    if not target_lang or target_lang == "en":
        return text
    try:
        return GoogleTranslator(source="en", target=target_lang).translate(text)
    except Exception as te:
        print("Translation error:", te)
        return text


# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------
@app.get("/api/transcribe")
def transcribe_youtube():
    url = request.args.get("url", "").strip()
    target_lang = request.args.get("target_lang", "en").strip().lower()

    if not url:
        return jsonify({"error": "Missing ?url"}), 400

    workdir = tempfile.mkdtemp(prefix="yt_subs_")
    try:
        audio_path = download_audio(url, workdir)

        segments_out = []
        segments, info = model.transcribe(audio_path, language="en", vad_filter=True)

        for seg in segments:
            text = maybe_translate(seg.text.strip(), target_lang)
            segments_out.append(
                {"start": float(seg.start), "end": float(seg.end), "text": text}
            )

        return jsonify(
            {
                "segments": segments_out,
                "srt": to_srt(segments_out),
                "vtt": to_vtt(segments_out),
                "duration": float(info.duration)
                if getattr(info, "duration", None) is not None
                else None,
                "language": target_lang,
            }
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


@app.post("/api/transcribe-file")
def transcribe_file():
    if "file" not in request.files:
        return jsonify({"error": "Missing file"}), 400

    target_lang = request.form.get("target_lang", "en").strip().lower()
    file = request.files["file"]

    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type"}), 400

    workdir = tempfile.mkdtemp(prefix="upload_subs_")
    try:
        input_path = os.path.join(workdir, file.filename)
        file.save(input_path)

        audio_path = extract_audio_from_file(input_path, workdir)

        segments_out = []
        segments, _info = model.transcribe(audio_path, language="en", vad_filter=True)

        for seg in segments:
            text = maybe_translate(seg.text.strip(), target_lang)
            segments_out.append(
                {"start": float(seg.start), "end": float(seg.end), "text": text}
            )

        return jsonify(
            {
                "segments": segments_out,
                "srt": to_srt(segments_out),
                "vtt": to_vtt(segments_out),
                "language": target_lang,
            }
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
