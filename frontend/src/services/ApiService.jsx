import axios from "axios";
import { profiles } from "../config/profiles";

const API_URL = (import.meta.env.VITE_API_URL || "https://aswproject.onrender.com/api").replace(
    /\/$/,
    "",
);

class APIService {
    constructor() {
        const savedApiKey = localStorage.getItem('currentApiKey');
        this.currentProfile = savedApiKey 
            ? profiles.find(p => p.apiKey === savedApiKey)
            : profiles[0];
    }

    setProfile(apiKey) {
        this.currentProfile = profiles.find(p => p.apiKey === apiKey);
        localStorage.setItem('currentApiKey', apiKey);
    }

    getHeaders() {
        return {
            'Accept': 'application/json',
            'Authorization': this.currentProfile.apiKey
        };
    }

    updateProfile(formData) {
        return this.post('/profile', formData);
    }

    // Eliminar el método deleteMedia específico y usar delete
    deleteMedia(mediaType) {
        return this.delete(`/profile/media/${mediaType}`);
    }
  
    get(route) {
        return axios.get(API_URL + route, { headers: this.getHeaders() });
    }
    
    post(route, body) {
        return axios.post(API_URL + route, body, { headers: this.getHeaders() });
    }

    put(route, body) {
        return axios.put(API_URL + route, body, { headers: this.getHeaders() });
    }

    delete(route) {
        return axios.delete(API_URL + route, { headers: this.getHeaders() });
    }
    
}

export default new APIService();
