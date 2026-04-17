// src/components/Profile.jsx
import React, { useState, useEffect } from "react";
import { profiles } from "../config/profiles";
import APIService from "../services/ApiService";
import Header from "./Header";
import "../styles/Profile.css";
import { formatDate } from '../utils/dateUtils';
import { Link } from 'react-router-dom';



const Profile = () => {
    const [selectedProfile, setSelectedProfile] = useState(
        localStorage.getItem('currentApiKey') || profiles[0].apiKey
    );
    const [profileData, setProfileData] = useState(null);
    const currentProfile = profiles.find(p => p.apiKey === selectedProfile);
    const [isEditingAbout, setIsEditingAbout] = useState(false);
    const [editedAbout, setEditedAbout] = useState('');
    const [profileImage, setProfileImage] = useState(null);
    const [bannerImage, setBannerImage] = useState(null);


    useEffect(() => {
        const loadProfileData = async () => {
            try {
                const response = await APIService.get("/profile");
                console.log("Datos del perfil recibidos:", response.data);
                
                // Usar los nombres correctos de las propiedades
                const profileData = {
                    ...response.data,
                    banner_url: response.data.banner_perfil_url,
                    profile_image_url: response.data.imagen_perfil_url
                };
                
                console.log("Datos procesados:", profileData);
                console.log("URL del banner:", profileData.banner_url);
                console.log("URL de la imagen:", profileData.profile_image_url);
                
                setProfileData(profileData);
            } catch (error) {
                console.error("Error loading profile:", error);
            }
        };
        
        loadProfileData();
    }, [selectedProfile]);

    const handleImageChange = (event, type) => {
        const file = event.target.files[0];
        if (type === 'profile') {
            setProfileImage(file);
        } else if (type === 'banner') {
            setBannerImage(file);
        }
    };

    const handleUpdateProfile = async (type) => {
        try {
            const formData = new FormData();
            
            if (type === 'profile' && profileImage) {
                formData.append('imagen', profileImage);
            } else if (type === 'banner' && bannerImage) {
                formData.append('banner', bannerImage);
            } else if (type === 'about' && editedAbout) {
                formData.append('about', editedAbout);
            }
    
            const response = await APIService.updateProfile(formData);
            
            if (response.data.profile) {
                setProfileData({
                    ...response.data.profile,
                    banner_url: response.data.profile.banner_perfil_url,
                    profile_image_url: response.data.profile.imagen_perfil_url
                });
            }
    
            // Limpiar estados
            if (type === 'profile') setProfileImage(null);
            if (type === 'banner') setBannerImage(null);
            if (type === 'about') {
                setEditedAbout('');
                setIsEditingAbout(false);
            }
    
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleProfileChange = (event) => {
        const newApiKey = event.target.value;
        setSelectedProfile(newApiKey);
        APIService.setProfile(newApiKey);
        window.location.reload();
    };

    const handleEditClick = () => {
        setEditedAbout(profileData?.about || '');
        setIsEditingAbout(true);
    };
    
   // Modificar la función handleSaveAbout para usar updateProfile
    const handleSaveAbout = async () => {
    try {
        const formData = new FormData();
        formData.append('about', editedAbout);
        
        const response = await APIService.updateProfile(formData);
        console.log('Respuesta del servidor:', response);
        
        if (response.data.profile) {
            setProfileData({
                ...response.data.profile,
                banner_url: response.data.profile.banner_perfil_url,
                profile_image_url: response.data.profile.imagen_perfil_url
            });
        }
        
        setIsEditingAbout(false);
    } catch (error) {
        console.error("Error actualizando about:", error);
    }
    };
    
    const handleCancelEdit = () => {
        setIsEditingAbout(false);
        setEditedAbout('');
    };

    const handleDeleteMedia = async (mediaType) => {
        try {
            const response = await APIService.deleteMedia(mediaType);
            
            if (response.data.profile) {
                setProfileData({
                    ...response.data.profile,
                    banner_url: response.data.profile.banner_perfil_url,
                    profile_image_url: response.data.profile.imagen_perfil_url
                });
            }
        } catch (error) {
            console.error(`Error al eliminar ${mediaType}:`, error);
            alert(`Error al eliminar ${mediaType}. Por favor, inténtalo de nuevo.`);
        }
    };


    return (
        <div className="main-container">
            
        <div className="profile-banner-wrapper">
            <div className="profile-banner">
                {console.log("Renderizando banner con URL:", profileData?.banner_perfil_url)}
                <img 
                    src={profileData?.banner_perfil_url || "https://aswimagenesfinal.s3.amazonaws.com/defaultbanner.png"} 
                    alt="Banner"
                    onError={(e) => {
                        console.log("Error cargando banner, usando default");
                        e.target.src = "https://aswimagenesfinal.s3.amazonaws.com/defaultbanner.png";
                    }}
                />
            </div>
            <div className="profile-picture">
                {console.log("Renderizando perfil con URL:", profileData?.imagen_perfil_url)}
                <img 
                    src={profileData?.imagen_perfil_url || "https://aswimagenesfinal.s3.amazonaws.com/default.jpg"} 
                    alt="Profile"
                    onError={(e) => {
                        console.log("Error cargando perfil, usando default");
                        e.target.src = "https://aswimagenesfinal.s3.amazonaws.com/default.jpg";
                    }}
                />
            </div>
        </div>

            <div className="profile-content">
                <div className="profile-selector">
                    <select value={selectedProfile} onChange={handleProfileChange}>
                        {profiles.map(profile => (
                            <option key={profile.apiKey} value={profile.apiKey}>
                                {profile.username}
                            </option>
                        ))}
                    </select>
                </div>

                <h1>Perfil de {currentProfile.username}</h1>
                <p className="profile-info"><strong>Karma:</strong> {profileData?.karma}</p>
                <p className="profile-info"><strong>Creado el:</strong> {profileData?.created_at ? formatDate(profileData.created_at) : ''}</p>
                <p className="profile-info"><strong>API Key:</strong> {selectedProfile}</p>

                <div className="profile-about-section">
                <h3>About</h3>
                {isEditingAbout ? (
                    <div className="about-edit">
                        <textarea
                            value={editedAbout}
                            onChange={(e) => setEditedAbout(e.target.value)}
                            className="about-textarea"
                        />
                        <div className="about-buttons">
                            <button className="action-button" onClick={handleSaveAbout}>Guardar</button>
                            <button className="action-button" onClick={handleCancelEdit}>Cancelar</button>
                        </div>
                    </div>
                ) : (
                    <div className="about-content">
                        {profileData?.about || 'Añade una descripción sobre ti'}
                        <button className="edit-button" onClick={handleEditClick}>
                            <i className="fas fa-edit"></i> Editar
                        </button>
                    </div>
                )}
            </div>

            <div className="profile-images-editor">
                <div className="profile-image-section">
                    <h3>Imagen de Perfil</h3>
                    <form onSubmit={(e) => {
                        e.preventDefault();
                        handleUpdateProfile('profile');
                    }}>
                        <input 
                            type="file" 
                            accept="image/*"
                            onChange={(e) => handleImageChange(e, 'profile')}
                        />
                        <button type="submit" className="action-button" disabled={!profileImage}>
                            Subir Imagen de Perfil
                        </button>
                    </form>
                    {profileData?.imagen_perfil_url && 
                    !profileData.imagen_perfil_url.includes('default.jpg') && (
                        <button 
                            className="action-button delete-button" 
                            onClick={() => handleDeleteMedia('image')}
                        >
                            Eliminar imagen de perfil
                        </button>
                    )}
                </div>
                
                <div className="profile-banner-section">
                    <h3>Banner de Perfil</h3>
                    <form onSubmit={(e) => {
                        e.preventDefault();
                        handleUpdateProfile('banner');
                    }}>
                        <input 
                            type="file" 
                            accept="image/*"
                            onChange={(e) => handleImageChange(e, 'banner')}
                        />
                        <button type="submit" className="action-button" disabled={!bannerImage}>
                            Subir Banner
                        </button>
                    </form>
                    {profileData?.banner_perfil_url && 
                    !profileData.banner_perfil_url.includes('defaultbanner.png') && (
                        <button 
                            className="action-button delete-button" 
                            onClick={() => handleDeleteMedia('banner')}
                        >
                            Eliminar banner
                        </button>
                    )}
                </div>
            </div>

                <div className="profile-links">
                    <a href={`/submissions/${currentProfile?.username}`}>Submissions</a>
                    <span className="separator">|</span>
                    <a href={`/comments/${currentProfile?.username}`}>Comments</a>
                    <span className="separator">|</span>
                    <a href="/hidden">Hidden Submissions</a>
                    <span className="separator">|</span>
                    <a href="/voted">Voted Submissions</a>
                    <span className="separator">|</span>
                    <a href="/voted-comments">Voted Comments</a>
                    <span className="separator">|</span>
                    <Link to={`/favorites/${currentProfile?.username}`}>Favorite Submissions</Link>
                    <span className="separator">|</span>
                    <a href={`/favorite-comments/${currentProfile?.username}`}>Favorite Comments</a>
                </div>
            </div>
        </div>
    );
};

export default Profile;