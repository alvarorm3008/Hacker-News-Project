# Frontend — ASW (React + Vite)

Interfaz web del clon tipo **Hacker News**: listados (news, newest, ask), envíos, comentarios, hilos y votos. Comunicación con el backend mediante **axios** y cabecera `Authorization` con la API key del usuario.

**Proyecto en grupo de 6** (ASW). Miembros: Carla Edo Garzon, Alvaro Rodriguez Martinez, Laia Belaustegui Colilaf, Carla Lopez Campos — *añade aquí los nombres 5 y 6*.

## Requisitos

- **Node.js** 18+ (recomendado LTS)
- npm (incluido con Node)

## Instalación

```bash
cd frontend
npm install
```

## Variables y API

La URL base de la API está definida en `src/services/ApiService.jsx` (constante `API_URL`).

- **Producción / despliegue:** por defecto apunta a `https://aswproject.onrender.com/api`.
- **Desarrollo local:** cambia `API_URL` a `http://127.0.0.1:8000/api` (o el puerto donde corra Django) mientras desarrollas.

Los perfiles de prueba y sus API keys están en `src/config/profiles.js`. En un entorno real conviene no versionar claves reales o cargarlas desde variables de entorno.

## Scripts

| Comando | Descripción |
|---------|-------------|
| `npm run dev` | Servidor de desarrollo (Vite) |
| `npm run build` | Build de producción en `dist/` |
| `npm run preview` | Previsualiza el build |
| `npm run start` | Sirve la carpeta `dist/` con `serve` (útil en despliegues tipo Render) |
| `npm run lint` | ESLint |

## Despliegue (referencia)

Ejemplo anterior: https://aswfrontend.onrender.com  

Suele usarse `npm run build` y un comando estático tipo `npm run start` o hosting de `dist/` en nginx, Netlify, Vercel, etc.

## Enlaces del proyecto

- **Taiga:** https://tree.taiga.io/project/carla172003-hn11a-asw-project

## Estructura principal

- `src/components/` — pantallas y piezas de UI
- `src/services/ApiService.jsx` — cliente HTTP hacia la API
- `src/config/profiles.js` — perfiles / API keys para pruebas
