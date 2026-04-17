import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from "react-router-dom";  // Importar useNavigate
import APIService from "../../services/ApiService";
import "../../styles/ReplyComment.css";

const ReplyComment = () => {
    const { id: parentCommentId } = useParams(); // Extraemos commentId desde la URL
    const [parentComment, setParentComment] = useState(null);
    const [replyText, setReplyText] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState('');
    const currentUser = APIService.currentProfile?.username;

    const navigate = useNavigate();  // Usamos el hook useNavigate

    // Obtener información del comentario padre al cargar el componente
    useEffect(() => {
        const fetchParentComment = async () => {
            try {
                const response = await APIService.get(`/comments/${parentCommentId}`);
                if (response.status === 200) {
                    setParentComment(response.data.comment); // Asumimos que la respuesta contiene la información del comentario
                } else {
                    setError('Error al cargar el comentario');
                }
            } catch (error) {
                setError('Error de red al obtener el comentario');
                console.error('Error de red:', error);
            }
        };

        fetchParentComment();
    }, [parentCommentId]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (replyText.trim() === '') return;

        const replyData = {
            text: replyText,
        };

        try {
            setIsSubmitting(true);
            setError('');

            // Llamada a la API para enviar la respuesta utilizando APIService
            const response = await APIService.post(`/comments/${parentCommentId}/reply`, replyData);

            if (response.status === 201) {
                console.log('Respuesta enviada exitosamente:', response.data);
                setReplyText(''); // Limpiar el campo de texto
                // Redirigir al detalle del comentario padre después de enviar la respuesta
                navigate(`/comment/${parentCommentId}`);  // Usamos navigate para redirigir
            } else {
                setError('Error al enviar la respuesta');
                console.error('Error al enviar respuesta:', response.data);
            }
        } catch (error) {
            setError('Error de red');
            console.error('Error de red:', error);
        } finally {
            setIsSubmitting(false);
        }
    };

    // Mostrar un mensaje de carga o error si no se ha cargado el comentario
    if (!parentComment) {
        return <div>Cargando comentario...</div>;
    }

    return (
        <div className="container-reply">
            {/* Detalles del comentario */}
            <div className="comment-details-parent">
                <strong className="author-info">
                    {parentComment.author === currentUser ? (
                        <a href="/profile" className="author-link">
                            <b>{parentComment.author}</b>
                        </a>
                    ) : (
                        <a href={`/author/${parentComment.author}/profile`} className="author-link">
                            {parentComment.author}
                        </a>
                    )}
                    {" "} | {" "}
                    <a href={`/comment/${parentComment.id}`} className="time-link">
                        {parentComment.time_ago}
                    </a>
                </strong>
                {" "} | on: {" "}
                <a href={`/submission/${parentComment.submission_id}`} className="submission-title">
                    {parentComment.submission_title}
                </a>
            </div>

            {/* Texto del comentario */}
            <p className="comment-text-parent">{parentComment.text}</p>

            {/* Mostrar errores si los hay */}
            {error && <div className="error-message">{error}</div>}

            {/* Formulario de respuesta */}
            <div className="reply-form">
                <form onSubmit={handleSubmit}>
                    <textarea
                        name="text"
                        rows="4"
                        cols="50"
                        className="reply-textarea"
                        value={replyText}
                        onChange={(e) => setReplyText(e.target.value)}
                        placeholder="Escribe tu respuesta aquí..."
                    />
                    <button
                        type="submit"
                        className="submit-reply-button"
                        disabled={isSubmitting}  // Deshabilitar el botón mientras se envía la respuesta
                    >
                        {isSubmitting ? 'Enviando...' : 'Reply'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default ReplyComment;
