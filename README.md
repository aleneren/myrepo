# Transcription App

A web app for transcribing audio files, built with a **React frontend** and **Flask backend**, containerised with Docker for easy local development.

## Architecture

```
┌─────────────────────┐        ┌──────────────────────┐        ┌─────────────┐
│   React Frontend    │ ──────▶│    Flask Backend     │ ──────▶│  OpenAI     │
│   (port 3000)       │        │    (port 8000)       │        │  Whisper    │
└─────────────────────┘        └──────────────────────┘        └─────────────┘
                                          │
                                          │
                                 ┌────────▼─────────┐
                                 │  SQLite Database │
                                 │  (local file,    │
                                 │   in backend)    │
                                 └──────────────────┘
```

**Why Flask + React?**

- **Flask** is lightweight and well-suited for a focused API service: minimal boilerplate, easy multipart file handling, and straightforward integration with Python audio tooling like `ffmpeg`
- **React** enables a responsive, stateful UI — tracking upload progress, errors, and results without page reloads

## Features

- 🎤 Drag-and-drop or click-to-upload audio files
- 📦 Batch upload up to 5 files at once
- 🔄 Automatic audio normalisation via `ffmpeg` (converts to mono 16kHz WAV before transcription)
- ✅ Per-file validation — unsupported formats and oversized files are rejected client-side before upload
- 📝 Transcription powered by OpenAI Whisper

**Supported formats:** MP3, MP4, MPEG, MPGA, M4A, WAV, WEBM · Max 25 MB per file

## Docker Setup

### Prerequisites

- Docker (Desktop, Colima, etc.)
- Docker Compose

### 1. Environment

```bash
cp frontend/sample.env frontend/.env
cp backend/sample.env backend/.env
```

Fill in each `.env` with your actual values — refer to the sample files for required variables.

### 2. Start

```bash
docker-compose up --build
```

| Service  | URL                   |
| -------- | --------------------- |
| Frontend | http://localhost:3000 |
| Backend  | http://localhost:8000 |

### Other Commands

```bash
docker-compose up        # start without rebuilding
docker-compose down      # stop and remove containers
docker-compose up --build  # rebuild after changes
```

---

For frontend-only or backend-only local development, see the respective [`frontend/`](frontend/README.md) and [`backend/`](backend/README.md) READMEs.
