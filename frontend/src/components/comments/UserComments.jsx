import React, { useState, useEffect } from "react"; 
import { useParams } from "react-router-dom";
import APIService from "../../services/ApiService";
import "../../styles/Threads.css";

const UserComments = () => {
    const { username } = useParams(); // Obtener username desde los parámetros de la URL
    const [userComments, setUserComments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    // Obtener el usuario actual desde el perfil de APIService
    const currentUser = APIService.currentProfile?.username;

    useEffect(() => {
        APIService.get(`/author/${username}/comments`)
            .then((response) => {
                setUserComments(response.data);
                setLoading(false);
            })
            .catch((err) => {
                setError("Error loading user comments");
                setLoading(false);
            });
    }, [username]); // El efecto depende del username

    const handleVote = (id) => {
        if (!userComments || userComments.length === 0) {
            console.error("Comments array is undefined or empty");
            return;
        }
    
        const comment = userComments.find((comment) => comment.id === id);
    
        if (!comment) {
            console.error(`Comment with id ${id} not found`);
            return;
        }
    
        const isVoting = !comment.has_voted; // Determina si es votar o quitar voto
        const apiUrl = `/comments/${id}/vote`;
    
        const apiCall = isVoting
            ? APIService.post(apiUrl) // Llamada POST para votar
            : APIService.delete(apiUrl); // Llamada DELETE para quitar voto
    
        apiCall
            .then(() => {
                // Actualiza solo el comentario votado sin hacer una llamada a la API para todos los comentarios
                setUserComments((prevComments) => 
                    prevComments.map((prevComment) =>
                        prevComment.id === id
                            ? {
                                  ...prevComment,
                                  has_voted: isVoting,
                                  points: isVoting
                                      ? prevComment.points + 1 // Incrementa puntos si vota
                                      : prevComment.points - 1, // Decrementa puntos si quita el voto
                              }
                            : prevComment
                    )
                );
            })
            .catch((error) => {
                console.error("Error managing vote:", error);
            });
    };
    
    

    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div className="threads-container">
            {userComments.length === 0 ? (
                <div className="comment no-comments">There are no comments yet.</div>
            ) : (
                userComments.map((comment) => (
                    <div key={comment.id} className="comment">
                        <div className="author">
                            {comment.author === currentUser ? (
                                <span className="author-asterisk" style={{ color: "orange", fontSize: "20px" }}>*</span> // Asterisco naranja
                            ) : (
                                <button
                                    className={`vote-button ${comment.has_voted ? "voted" : ""}`}
                                    onClick={() => handleVote(comment.id)}
                                >
                                    {comment.has_voted ? "Unvote" : "Vote"}
                                </button>
                            )}
                            <span className="points">{comment.points} points </span>
                            by {comment.author === currentUser ? (
                                <a href="/profile" className="author-link">
                                    <b>{comment.author}</b>
                                </a>
                            ) : (
                                <a href={`/author/${comment.author}/profile`} className="author-link">
                                    {comment.author}
                                </a>
                            )}
                            {" "} | <a href={`/comment/${comment.id}`}>{comment.time_ago}</a> |
                            on: <a href={`/submission/${comment.submission_id}`}>{comment.submission_title}</a>
                            {comment.author === currentUser && (
                                <span>
                                    | <a href={`/comments/${comment.id}/edit`} className="author-link">edit</a> |
                                    <a href={`/comments/${comment.id}/delete`} className="author-link">delete</a>
                                </span>
                            )}
                            
                        </div>
                        <div className="text">{comment.text}</div>
                    </div>
                ))
            )}
        </div>
    );
};

export default UserComments;
