# Hacker News — Frontend (React + Vite)

SPA del clon tipo **Hacker News**: listados (news, newest, ask), envíos, comentarios, hilos y votos. Consume la API con **axios** y envía la **API key** en la cabecera `Authorization`.

Este código vive en el monorepo bajo la carpeta **`frontend/`**.

---

## Contenido

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Variables de entorno](#variables-de-entorno)
- [Scripts](#scripts)
- [Estructura](#estructura)

---

## Requisitos

| Entorno | Versión recomendada |
|--------|---------------------|
| Node.js | 18+ (LTS) |
| npm | Incluido con Node |

---

## Instalación

```bash
cd frontend
npm install
```

Arranque en desarrollo:

```bash
npm run dev
```

---

## Variables de entorno

Copia **`.env.example`** a **`.env.local`** (no lo subas al repositorio). Vite solo expone variables con prefijo **`VITE_`**.

- **`VITE_API_URL`**: URL base de la API (por ejemplo `http://127.0.0.1:8000/api`). Si no se define, el cliente usa la URL de despliegue por defecto definida en código.
- **`VITE_API_KEY_*`**: claves por perfil; se consumen en `src/config/profiles.js`.

---

## Scripts

| Comando | Descripción |
|---------|-------------|
| `npm run dev` | Servidor de desarrollo (Vite) |
| `npm run build` | Build de producción en `dist/` |
| `npm run preview` | Previsualiza el build |
| `npm run start` | Sirve `dist/` con `serve` |
| `npm run lint` | ESLint |

---

## Estructura

| Ruta | Rol |
|------|-----|
| `src/components/` | Pantallas y UI |
| `src/services/ApiService.jsx` | Cliente HTTP |
| `src/config/profiles.js` | Perfiles y API keys (desde env) |
