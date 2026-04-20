# Hacker News — Frontend (React + Vite)

SPA for the **Hacker News-style** clone: listings (`news`, `newest`, `ask`), submissions, comments, threads, and voting. It consumes the API with **axios** and sends the **API key** in the `Authorization` header.

This code lives in the monorepo under **`frontend/`**.

---

## Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Scripts](#scripts)
- [Structure](#structure)

---

## Requirements

| Environment | Recommended Version |
|-------------|---------------------|
| Node.js | 18+ (LTS) |
| npm | Included with Node |

---

## Installation

```bash
cd frontend
npm install
```

Start in development mode:

```bash
npm run dev
```

---

## Environment Variables

Copy **`.env.example`** to **`.env.local`** (do not commit it). Vite only exposes variables with the **`VITE_`** prefix.

- **`VITE_API_URL`**: Base API URL (for example `http://127.0.0.1:8000/api`). If not defined, the client uses the default deployed URL defined in code.
- **`VITE_API_KEY_*`**: profile keys consumed in `src/config/profiles.js`.

---

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Development server (Vite) |
| `npm run build` | Production build in `dist/` |
| `npm run preview` | Preview the production build |
| `npm run start` | Serve `dist/` using `serve` |
| `npm run lint` | ESLint |

---

## Structure

| Path | Role |
|------|------|
| `src/components/` | Views and UI |
| `src/services/ApiService.jsx` | HTTP client |
| `src/config/profiles.js` | Profiles and API keys (from env) |
