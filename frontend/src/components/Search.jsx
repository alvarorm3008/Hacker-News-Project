import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import APIService from '../services/ApiService';
import Header from './Header';

const Search = () => {
    const [results, setResults] = useState([]);  // Inicializado como array vacío
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const location = useLocation();
    const searchQuery = new URLSearchParams(location.search).get('q');
    const currentUser = APIService.currentProfile?.username;

    useEffect(() => {
        const fetchResults = async () => {
            try {
                console.log('Buscando con query:', searchQuery);
                const response = await APIService.get(`/newest?query=${encodeURIComponent(searchQuery)}`);
                console.log('Respuesta completa:', response);
                console.log('Datos recibidos:', response.data);
                
                // Si la respuesta es un objeto con una propiedad que contiene el array
                let submissionsArray;
                if (Array.isArray(response.data)) {
                    submissionsArray = response.data;
                } else if (typeof response.data === 'object') {
                    // Buscar la primera propiedad que sea un array
                    const arrayProperty = Object.values(response.data).find(val => Array.isArray(val));
                    submissionsArray = arrayProperty || [];
                } else {
                    submissionsArray = [];
                }
    
                console.log('Submissions procesadas:', submissionsArray);
                setResults(submissionsArray);
                setLoading(false);
            } catch (error) {
                console.error('Error detallado:', {
                    message: error.message,
                    response: error.response,
                    data: error.response?.data
                });
                setError('Error buscando submissions');
                setLoading(false);
            }
        };
    
        if (searchQuery) {
            fetchResults();
        } else {
            setResults([]);
            setLoading(false);
        }
    }, [searchQuery]);

    if (loading) return <div>Buscando...</div>;
    if (error) return <div>{error}</div>;
    if (!results.length) return <div>No se encontraron resultados para: {searchQuery}</div>;

    return (
        <div className="main-container">
            <Header />
            <div className="submissions-container">
                <h2>Resultados para: {searchQuery}</h2>
                {results.map((submission) => (
                    <div key={submission.id} className="container">
                        <div className="news-item">
                            <div className="news-content">
                                {submission.author !== currentUser && (
                                    <button
                                        className={`vote-button ${submission.has_voted ? "voted" : ""}`}
                                        onClick={() => handleVote(submission.id, submission.has_voted)}
                                    >
                                        {submission.has_voted ? "Unvote" : "Vote"}
                                    </button>
                                )}
                                <div className="title-container">
                                    <a href={`/submission/${submission.id}`} className="news-title">
                                        {submission.title}
                                    </a>
                                </div>
                            </div>
                            <div className="author-points-container">
                                <span className="points">{submission.points} points</span>
                                <span className="author">
                                    by{" "}
                                    {submission.author === currentUser ? (
                                        <a href="/profile" className="author-link">
                                            <b>{submission.author}</b>
                                        </a>
                                    ) : (
                                        <a href={`/author/${submission.author}/profile`} className="author-link">
                                            {submission.author}
                                        </a>
                                    )}
                                    {" | "}
                                    <a href={`/submission/${submission.id}`}>{submission.time_ago}</a>
                                    {" | "}
                                    {submission.num_comments}
                                </span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Search;