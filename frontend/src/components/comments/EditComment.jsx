import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom"; // Eliminamos useNavigate
import APIService from "../../services/ApiService"; // Ruta al archivo de tu API service
import "../../styles/EditComment.css"; // Importando el CSS adaptado

const EditComment = () => {
    const { id: commentId } = useParams(); // Extraemos commentId desde la URL
    const [comment, setComment] = useState(null);
    const [updatedText, setUpdatedText] = useState(""); // Estado para el nuevo texto del comentario
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

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
                    setUpdatedText(commentData.text); // Inicializar el texto del comentario
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

    // Manejar la actualización del comentario
    const handleUpdate = async () => {
        try {
            // Hacemos la llamada PUT, enviando el cuerpo como JSON
            const response = await APIService.put(
                `/comments/${commentId}/edit`, 
                { text: updatedText },  // El cuerpo contiene el nuevo texto
            );

            if (response.status === 200) {
                alert("Comment updated successfully.");

                // Actualizamos el comentario en la misma página
                setComment(prevComment => ({
                    ...prevComment,
                    text: updatedText
                }));
            } else {
                alert("An error occurred while updating the comment.");
            }
        } catch (error) {
            if (error.response?.status === 400) {
                alert("Invalid request. Please check the input data.");
            } else if (error.response?.status === 403) {
                alert("You do not have permission to edit this comment.");
            } else if (error.response?.status === 404) {
                alert("Comment not found.");
            } else {
                alert("An unexpected error occurred.");
            }
            console.error(error); // Para ver detalles de errores en consola
        }
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
                    </a>{" "}
                    <a href={`/comment/${comment.id}`}>{comment.time_ago}</a> |{" "}
                    on:{" "}
                    <a href={`/submission/${comment.submission_id}`}>{comment.submission_title}</a>
                    {" "}
                    <span>
                        | {" "}
                        <a href={`/comments/${comment.id}/edit`} className="author-link">
                            edit
                        </a>{" "} | {" "}
                        <a href={`/comments/${comment.id}/delete`} className="author-link">
                            delete
                        </a>
                    </span>
                </div>

                {/* Mostrar el texto original del comentario */}
                <div className="original-comment-text">
                    <p>{comment?.text}</p>
                </div>

                {/* Campo para editar el comentario */}
                <div className="text">
                    <textarea
                        value={updatedText}
                        onChange={(e) => setUpdatedText(e.target.value)} // Actualiza el texto
                        rows="5"
                        className="edit-textarea"
                    />
                </div>

                {/* Botón para actualizar el comentario */}
                <div>
                    <button onClick={handleUpdate} className="update-button">
                        Update
                    </button>
                </div>
            </div>
        </div>
    );
};

export default EditComment;
