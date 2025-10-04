import { useEffect, useRef, useState } from "react";

// Helper: load YouTube IFrame API once
function useYouTubeApi() {
  const [ready, setReady] = useState(false);
  useEffect(() => {
    if (window.YT && window.YT.Player) {
      setReady(true);
      return;
    }
    const existing = document.getElementById("youtube-iframe-api");
    if (!existing) {
      const tag = document.createElement("script");
      tag.src = "https://www.youtube.com/iframe_api";
      tag.id = "youtube-iframe-api";
      document.body.appendChild(tag);
    }
    window.onYouTubeIframeAPIReady = () => setReady(true);
  }, []);
  return ready;
}

export default function App() {
  const apiReady = useYouTubeApi();
  const playerRef = useRef(null);
  const rafRef = useRef(null);

  const [url, setUrl] = useState("");
  const [videoId, setVideoId] = useState("");
  const [segments, setSegments] = useState([]); // [{start, end, text}]
  const [currentText, setCurrentText] = useState("");
  const [loading, setLoading] = useState(false);
  const [vttText, setVttText] = useState("");
  const [srtText, setSrtText] = useState("");
  const [showSubs, setShowSubs] = useState(true);
  const [lang, setLang] = useState("en"); // NEW: target language dropdown

  // Extract YouTube video ID from common URL formats
  function extractVideoId(link) {
    try {
      const u = new URL(link);
      if (u.hostname.includes("youtu.be")) return u.pathname.replace("/", "");
      if (u.searchParams.get("v")) return u.searchParams.get("v");
      const m = link.match(/(?:v=|\/embed\/|\/v\/|youtu\.be\/)([\w-]{11})/);
      return m ? m[1] : "";
    } catch {
      const m = link.match(/([\w-]{11})/);
      return m ? m[1] : "";
    }
  }

  // Initialize YT player when apiReady & videoId
  useEffect(() => {
    if (!apiReady || !videoId) return;
    if (playerRef.current) {
      playerRef.current.destroy?.();
    }
    playerRef.current = new window.YT.Player("player", {
      videoId,
      playerVars: { modestbranding: 1, rel: 0, playsinline: 1 },
      events: {
        onReady: () => {
          cancelAnimationFrame(rafRef.current);
          const loop = () => {
            try {
              const t = playerRef.current?.getCurrentTime?.() || 0;
              const seg = segments.find((s) => t >= s.start && t <= s.end);
              setCurrentText(seg ? seg.text : "");
            } catch {}
            rafRef.current = requestAnimationFrame(loop);
          };
          loop();
        },
      },
    });
    return () => cancelAnimationFrame(rafRef.current);
  }, [apiReady, videoId, segments]);

  async function handleTranscribe(e) {
    e.preventDefault();
    const id = extractVideoId(url);
    if (!id) {
      alert("Please enter a valid YouTube URL.");
      return;
    }

    setVideoId(id);
    setLoading(true);
    try {
      // Send target language to backend
      const resp = await fetch(
        `/api/transcribe?url=${encodeURIComponent(url)}&target_lang=${lang}`
      );
      if (!resp.ok) throw new Error("Transcription failed");
      const data = await resp.json();
      setSegments(data.segments || []);
      setVttText(data.vtt || "");
      setSrtText(data.srt || "");
    } catch (err) {
      console.error(err);
      alert("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ padding: 20, color: "white", background: "#111", minHeight: "100vh" }}>
      <h1>YouTube Auto Subtitles</h1>
      <form onSubmit={handleTranscribe}>
        <input
          type="text"
          placeholder="Paste YouTube link..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{ width: "400px", marginRight: "10px" }}
        />

        {/* NEW: Language dropdown */}
        <select
          value={lang}
          onChange={(e) => setLang(e.target.value)}
          style={{ marginRight: "10px" }}
        >
          <option value="en">English</option>
          <option value="bg">Bulgarian</option>
          <option value="es">Spanish</option>
          <option value="fr">French</option>
          <option value="de">German</option>
          <option value="it">Italian</option>
          <option value="ru">Russian</option>
          <option value="zh">Chinese</option>
          {/* Add more language codes as needed */}
        </select>

        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate"}
        </button>
      </form>

      <div id="player" style={{ marginTop: 20, width: "640px", height: "360px" }}></div>

      {showSubs && currentText && (
        <div style={{ marginTop: 20, fontSize: "18px", background: "#222", padding: "10px" }}>
          {currentText}
        </div>
      )}

      {srtText && (
        <div style={{ marginTop: 20 }}>
          <a
            href={`data:text/plain;charset=utf-8,${encodeURIComponent(srtText)}`}
            download="subtitles.srt"
          >
            Download .srt
          </a>{" "}
          |{" "}
          <a
            href={`data:text/plain;charset=utf-8,${encodeURIComponent(vttText)}`}
            download="subtitles.vtt"
          >
            Download .vtt
          </a>
        </div>
      )}
    </div>
  );
}
