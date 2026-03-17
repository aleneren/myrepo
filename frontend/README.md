# Frontend

React Router v7 app with TypeScript.

**Note:** This project is designed to run locally or via Docker. Do **not** run local development and Docker at the same time — they may conflict on ports.

---

## Local Development

**Requirements:** Node.js 20+

### Setup

1. Create a `.env` file in `frontend/` using [`sample.env`](sample.env) as reference:
```bash
   cp sample.env .env
```

2. Install dependencies — **do this before running any other commands**:
```bash
   npm ci
```

### Development

```bash
npm run dev
```

Your application will be available at `http://127.0.0.1:3000`.

### Build

```bash
npm run build
npm run start
```

### Testing

```bash
npm run test
```

### Type Checking

```bash
npm run typecheck
```

## Building for Production

Create a production build:

```bash
npm run build
```

## Docker Deployment (Frontend + Backend)

This project is designed to run via Docker. For running **both frontend and backend together**, use the **root Docker setup**:

[Refer to the project root README](../README.md) for full instructions on building and running the application via Docker Compose.

### Quick Start from Project Root

```bash
docker-compose up --build
```

---

Built with ❤️ using React Router.
