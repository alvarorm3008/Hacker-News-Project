// src/components/UserProfile.jsx
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import APIService from "../services/ApiService";
import Header from "./Header";
import "../styles/Profile.css";
import { formatDate } from '../utils/dateUtils';

const UserProfile = () => {
    const { username } = useParams();
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadUserData = async () => {
            try {
                console.log('Intentando cargar perfil para:', username); // Debug
                const response = await APIService.get(`/author/${username}/profile`);
                console.log('Respuesta:', response.data); // Debug
                setUserData(response.data);
                setLoading(false);
            } catch (error) {
                console.error("Error detallado:", {
                    message: error.message,
                    status: error.response?.status,
                    data: error.response?.data
                });
                setError(error.response?.status === 404 
                    ? `No se encontró el perfil del usuario ${username}` 
                    : 'Error al cargar el perfil');
                setLoading(false);
            }
        };
        
        loadUserData();
    }, [username]);

    if (loading) return <div className="loading">Cargando perfil...</div>;
    if (error) return (
        <div className="main-container">
            <Header />
            <div className="error-container">
                <h2>Error</h2>
                <p>{error}</p>
                <Link to="/" className="back-link">Volver al inicio</Link>
            </div>
        </div>
    );

    return (
        <div className="main-container">
            
            <div className="profile-banner-wrapper">
                <div className="profile-banner">
                    <img 
                        src={userData?.banner_perfil_url || "https://aswimagenesfinal.s3.amazonaws.com/defaultbanner.png"} 
                        alt="Banner"
                    />
                </div>
                <div className="profile-picture">
                    <img 
                        src={userData?.imagen_perfil_url || "https://aswimagenesfinal.s3.amazonaws.com/default.jpg"} 
                        alt="Profile"
                    />
                </div>
            </div>

            <div className="profile-content">
                <h1>Perfil de {userData?.username}</h1>
                <p className="profile-info"><strong>Karma:</strong> {userData?.karma}</p>
                <p className="profile-info"><strong>Creado el:</strong> {userData?.created_at ? formatDate(userData.created_at) : ''}</p>
                <div className="profile-about-section">
                    <h3>About</h3>
                    <p>{userData?.about || 'Este usuario no tiene descripción.'}</p>
                </div>

                <div className="profile-links">
                    <a href={`/submissions/${username}`}>Submissions</a>
                    <span className="separator">|</span>
                    <a href={`/comments/${username}`}>Comments</a>
                    <span className="separator">|</span>                    
                    <a href={`/favorites/${userData?.username}`}>Favorite Submissions</a>
                    <span className="separator">|</span>
                    <a href={`/favorite-comments/${username}`}>Favorite Comments</a>
                </div>
            </div>
        </div>
    );
};

export default UserProfile;