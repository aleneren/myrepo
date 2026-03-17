import React, { useState } from "react";
import { createPortal } from "react-dom";
import "./TranscriptionsList.css";

interface Transcription {
  id: number;
  filename: string;
  transcription: string;
  created_at: string;
}

interface TranscriptionsListProps {
  transcriptions: Transcription[];
}

const formatDate = (s: string) => {
  try {
    return new Date(s).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return s;
  }
};

const TranscriptionsList: React.FC<TranscriptionsListProps> = ({
  transcriptions,
}) => {
  const [toastKey, setToastKey] = useState(0);

  const handleCopy = async (text: string, id: number) => {
    try {
      await navigator.clipboard.writeText(text);
      setToastKey((k: number) => k + 1); // forces a fresh mount each click
      setTimeout(() => setToastKey(0), 2000);
    } catch {
      /* fail silently */
    }
  };

  if (transcriptions.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-icon">📝</div>
        <h3>No transcriptions yet</h3>
        <p>Upload some audio files to get started!</p>
      </div>
    );
  }

  return (
    <div className="transcriptions-list">
      <p className="list-count">
        {transcriptions.length} transcription
        {transcriptions.length !== 1 ? "s" : ""}
      </p>

      {transcriptions.map((t) => (
        <div key={t.id} className="transcription-card">
          <div className="card-header">
            <div className="file-info">
              <h4 className="filename" title={t.filename}>
                🎵 {t.filename}
              </h4>
              <span className="created-date">{formatDate(t.created_at)}</span>
            </div>
            <button
              className="copy-button"
              onClick={() => handleCopy(t.transcription, t.id)}
              title="Copy transcription"
            >
              📋
            </button>
          </div>

          <div className="card-body">
            <p className="transcription-text">{t.transcription}</p>
          </div>

          <div className="card-footer">
            <span>📝 {t.transcription.length} chars</span>
            <span>
              💬 {t.transcription.split(/\s+/).filter(Boolean).length} words
            </span>
          </div>
        </div>
      ))}

      {toastKey !== 0 &&
        createPortal(
          <div key={toastKey} className="copy-toast">
            Copied!
          </div>,
          document.body,
        )}
    </div>
  );
};

export default TranscriptionsList;
