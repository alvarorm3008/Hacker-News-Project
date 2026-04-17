import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom"; // Añadir useNavigate
import APIService from "../../services/ApiService"; // Ruta al archivo de tu API service
import "../../styles/CommentDetail.css"; // Importando el CSS adaptado

const DeleteComment = () => {
    const { id: commentId } = useParams(); // Extraemos commentId desde la URL
    const [comment, setComment] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate(); // Inicializamos el hook navigate

    // Cargar datos del comentario al montar el componente
    useEffect(() => {
        const fetchComment = async () => {
            try {
                const response = await APIService.get(`/comments/${commentId}`);
                console.log(response.data); // Verifica la respuesta completa aquí

                // Aseguramos que los datos están en la estructura correcta
                const commentData = response.data?.comment;
                if (commentData) {
                    setComment(commentData); // Asignar el comentario
                } else {
                    setError("Comment not found.");
                }
            } catch (err) {
                setError("Error loading comment.");
                console.error(err);  // Para ver detalles de errores en consola
            } finally {
                setIsLoading(false);
            }
        };

        fetchComment();
    }, [commentId]);

    const handleDelete = async () => {
        try {
            const response = await APIService.delete(`/comments/${commentId}`);
            if (response.status === 204) {
                alert("Comment deleted successfully.");
                navigate("/comments"); // Redirige a la página de comentarios
            } else {
                alert("An error occurred while deleting the comment.");
            }
        } catch (error) {
            if (error.response?.status === 403) {
                alert("You do not have permission to delete this comment.");
            } else if (error.response?.status === 404) {
                alert("Comment not found.");
            } else {
                alert("An unexpected error occurred.");
            }
        }
    };

    // Redirigir a la página de comentarios si el usuario decide no eliminar
    const handleCancel = () => {
        navigate("/comments"); // Redirige a la página de comentarios
    };

    if (isLoading) {
        return <p>Loading comment...</p>;
    }

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <div className="threads-container">
            <div className="container">
                <div className="author">
                    <span className="orange-asterisk">*</span>
                    <span className="points">{comment?.points} points</span> by{" "}
                    <a href="/profile" className="author-link">
                        <b>{comment.author}</b>
                    </a>
                    {" "}
                    <a href={`/comment/${comment.id}`}>{comment.time_ago}</a> |{" "}
                    on:{" "}
                    <a href={`/submission/${comment.submission_id}`}>{comment.submission_title}</a>
                    {" "} 
                    <span>
                        | {" "}
                        <a href={`/comments/${comment.id}/edit`} className="author-link">
                            edit
                        </a>
                        {" "} | {" "}

                        <a href={`/comments/${comment.id}/delete`} className="author-link">
                            delete
                        </a>
                    </span>
                </div>
                <div className="text">{comment?.text || "No text available."}</div>
    

                {/* Confirmación de eliminación */}
                <div className="confirm-delete">
                    <p>Do you want this to be deleted?</p>
                    <button className="btn-confirm" onClick={handleDelete}>
                        Yes
                    </button>
                    <button className="btn-cancel" onClick={handleCancel}>
                        No
                    </button>
                </div>
            </div>
        </div>
    );
};

export default DeleteComment;
