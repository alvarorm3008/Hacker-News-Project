// API keys per profile: set in .env.local (see frontend/.env.example). Never commit real keys.

const env = import.meta.env;

export const profiles = [
  {
    username: "pes",
    apiKey: env.VITE_API_KEY_PES || "",
  },
  {
    username: "laia",
    apiKey: env.VITE_API_KEY_LAIA || "",
  },
  {
    username: "laia6",
    apiKey: env.VITE_API_KEY_LAIA6 || "",
  },
  {
    username: "carla",
    apiKey: env.VITE_API_KEY_CARLA || "",
  },
];
