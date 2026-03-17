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

### Quick Start

Start both frontend and backend services:

```bash
docker-compose up --build
```

Access:

- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### Development

```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up --build
```
