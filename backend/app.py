import os
import tempfile
import shutil
from flask import Flask, request, jsonify
from faster_whisper import WhisperModel
import yt_dlp
from deep_translator import GoogleTranslator

# Model choice: "small", "medium", "large-v3" (bigger = slower, more accurate)
MODEL_SIZE = os.getenv("WHISPER_MODEL", "small")
COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE_TYPE", "int8")  # e.g., float16 on GPU

app = Flask(__name__)
model = WhisperModel(MODEL_SIZE, compute_type=COMPUTE_TYPE)


def download_audio(youtube_url: str, out_dir: str) -> str:
    """Download audio track and return the filepath to a WAV/MP3."""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(out_dir, "%(id)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "noplaylist": True,
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        basename = f"{info['id']}.mp3"
        path = os.path.join(out_dir, basename)
        if not os.path.exists(path):
            raise FileNotFoundError("Audio not found after download.")
        return path


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
        lines.append(s['text'].strip())
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
        lines.append(s['text'].strip())
        lines.append("")
    return "\n".join(lines)


@app.get("/api/transcribe")
def transcribe():
    url = request.args.get("url", "").strip()
    target_lang = request.args.get("target_lang", "en").strip().lower()  # default English

    if not url:
        return jsonify({"error": "Missing ?url"}), 400

    workdir = tempfile.mkdtemp(prefix="yt_subs_")
    try:
        audio_path = download_audio(url, workdir)
        segments_out = []

        # Transcribe in English
        segments, info = model.transcribe(audio_path, language="en", vad_filter=True)

        for seg in segments:
            text = seg.text.strip()

            # Translate if needed
            if target_lang != "en":
                try:
                    text = GoogleTranslator(source="en", target=target_lang).translate(text)
                except Exception as te:
                    print("Translation error:", te)

            segments_out.append({
                "start": float(seg.start),
                "end": float(seg.end),
                "text": text,
            })

        # Build caption files
        srt = to_srt(segments_out)
        vtt = to_vtt(segments_out)

        return jsonify({
            "segments": segments_out,
            "srt": srt,
            "vtt": vtt,
            "duration": float(info.duration) if getattr(info, 'duration', None) else None,
            "language": target_lang,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
