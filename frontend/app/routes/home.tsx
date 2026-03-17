import type { Route } from "./+types/home";
import { useState, useEffect } from "react";
import FileUpload from "../components/FileUpload";
import SearchBar from "../components/SearchBar";
import TranscriptionsList from "../components/TranscriptionsList";
import { BACKEND_URL } from "../const";

const HEALTH_TIMEOUT_MS = 30000;
const HEALTH_POLL_MS = 2000;

export function meta({}: Route.MetaArgs) {
  return [
    { title: "Audio Transcription - AI Powered" },
    {
      name: "description",
      content:
        "Upload audio files and get AI-powered transcriptions using Whisper",
    },
  ];
}

interface Transcription {
  id: number;
  filename: string;
  transcription: string;
  created_at: string;
}

type HealthStatus = "loading" | "ready" | "timeout";

export default function Home() {
  const [health, setHealth] = useState<HealthStatus>("loading");
  const [transcriptions, setTranscriptions] = useState<Transcription[]>([]);
  const [filtered, setFiltered] = useState<Transcription[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let stopped = false;
    const start = Date.now();

    const poll = async () => {
      while (!stopped) {
        try {
          const res = await fetch(`${BACKEND_URL}/health`);
          if (res.ok) {
            setHealth("ready");
            return;
          }
        } catch {
          /* not ready yet */
        }

        if (Date.now() - start >= HEALTH_TIMEOUT_MS) {
          setHealth("timeout");
          return;
        }

        await new Promise((r) => setTimeout(r, HEALTH_POLL_MS));
      }
    };

    poll();
    return () => {
      stopped = true;
    };
  }, []);

  useEffect(() => {
    if (health === "ready") fetchTranscriptions();
  }, [health]);

  const fetchTranscriptions = async () => {
    try {
      setLoading(true);
      const data = await fetch(`${BACKEND_URL}/transcriptions`).then((r) =>
        r.json(),
      );
      setTranscriptions(data);
      setFiltered(data);
    } catch {
      setError("Failed to fetch transcriptions");
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = async () => {
    await fetchTranscriptions();
  };

  const handleSearch = async (query: string) => {
    if (!query.trim()) {
      setFiltered(transcriptions);
      return;
    }
    try {
      const data = await fetch(
        `${BACKEND_URL}/search?query=${encodeURIComponent(query)}`,
      ).then((r) => r.json());
      setFiltered(data);
    } catch {
      setError("Search failed");
    }
  };

  if (health === "loading") {
    return (
      <div className="home-page">
        <div className="health-screen">
          <div className="health-spinner" />
          <h2>Starting up…</h2>
          <p>Waiting for the server to become ready</p>
        </div>
      </div>
    );
  }

  if (health === "timeout") {
    return (
      <div className="home-page">
        <div className="health-screen">
          <div className="health-timeout-icon">⚠️</div>
          <h2>Server unavailable</h2>
          <p>
            Could not reach the server after {HEALTH_TIMEOUT_MS / 1000} seconds.
          </p>
          <button className="retry-button" onClick={() => setHealth("loading")}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="home-page">
      <header className="hero-section">
        <h1>🎵 Audio Transcription</h1>
        <p>
          Upload up to 5 audio files and get AI-powered transcriptions using
          Whisper
        </p>
      </header>

      <main className="main-content">
        <section className="upload-section">
          <FileUpload onUploadSuccess={handleUploadSuccess} />
        </section>

        <section className="transcriptions-section">
          <SearchBar onSearch={handleSearch} />
          {loading && <div className="loading">Loading transcriptions...</div>}
          {error && <div className="error">{error}</div>}
          <div className="transcriptions-scroll">
            <TranscriptionsList transcriptions={filtered} />
          </div>
        </section>
      </main>
    </div>
  );
}
