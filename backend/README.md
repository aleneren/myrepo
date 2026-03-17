# Backend

Flask API for transcription service.

**Note:** Use either Docker (via docker-compose from the root directory) **OR** local development — do not run both simultaneously as they use the same ports.

---

## Local Development

**Requirements:** Python 3.10+

## Local Development

**Requirements:** Python 3.10+

### Setup

1. Create a `.env` file in `backend/` using [`sample.env`](sample.env) as reference:
```bash
   cp sample.env .env
```

2. Create and activate a virtual environment:

   #### macOS / Linux
```bash
   python -m venv venv
   source venv/bin/activate
```

   #### Windows
```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
```

3. Install requirements — **do this before running any other commands**:
```bash
   pip install --upgrade pip
   pip install -r requirements.txt
```

### Run Server
```bash
python run.py
```

API runs on http://localhost:8000

### Testing

```bash
python -m pytest
```

## Docker Deployment (Frontend + Backend)

This project is designed to run via Docker. For running **both frontend and backend together**, use the **root Docker setup**:

[Refer to the project root README](../README.md) for full instructions on building and running the application via Docker Compose.

### Quick Start from Project Root

```bash
docker-compose up --build
```
