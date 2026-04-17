import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import APIService from "../../services/ApiService";
import "../../styles/CommentDetail.css";

// Componente recursivo para mostrar un árbol de respuestas sin incluir el comentario padre
const CommentTree = ({ comment }) => {
    const currentUser = APIService.currentProfile?.username;
    const [isFavorite, setIsFavorite] = useState(false);

    const handleVote = () => {
        const isVoting = !comment.has_voted;
        const apiCall = isVoting
            ? APIService.post(`/comments/${comment.id}/vote`)
            : APIService.delete(`/comments/${comment.id}/vote`);

        apiCall
            .then(() => {
                // Actualiza el comentario para reflejar el voto
                comment.has_voted = isVoting;
                comment.points = isVoting ? comment.points + 1 : comment.points - 1;
            })
            .catch((error) => console.error("Error managing vote:", error));
    };
    // Pendiente de revisar
    const toggleFavorite = () => {
        const apiCall = isFavorite
            ? APIService.delete(`/comments/${comment.id}/favorite`)
            : APIService.post(`/comments/${comment.id}/favorite`);

        apiCall
            .then(() => setIsFavorite((prev) => !prev))
            .catch(() => console.error("Error toggling favorite"));
    };

    return (
        <div className="comment-tree">
            <div className="comment-node">
                <div className="author">
                    {comment.author === currentUser ? (
                        <span
                            className="author-asterisk"
                            style={{ color: "orange", fontSize: "20px" }}
                        >
                            *
                        </span>
                    ) : (
                        <button
                            className={`vote-button ${comment.has_voted ? "voted" : ""}`}
                            onClick={() => handleVote()}
                        >
                            {comment.has_voted ? "Unvote" : "Vote"}
                        </button>
                    )}
                    <span className="points">{comment.points} points</span>{" "}
                    by{" "}
                    <a href={`/author/${comment.author}/profile`} className="author-link">
                        {comment.author}
                    </a>{" "}
                    |{" "}
                    <a href={`/comment/${comment.id}`}>{comment.time_ago}</a> |{" "}
                    <a
                        href="#"
                        className="favorite-link"
                        onClick={(e) => {
                            e.preventDefault();
                            toggleFavorite();
                        }}
                    >
                        {isFavorite ? "un-favorite" : "favorite"}
                    </a>{" "}
                    {comment.author === currentUser && (
                        <>
                            {" "}|{" "}
                            <a href={`/comments/${comment.id}/edit`} className="edit-link">
                                edit
                            </a>{" "} |{" "}
                            <a
                                href={`/comments/${comment.id}/delete`}
                                className="delete-link"
                            >
                                delete
                            </a>
                        </>
                    )}
                </div>
                <div className="text">{comment.text}</div>
                <a href={`/comments/${comment.id}/reply`} className="reply-link">
                    Reply
                </a>
            </div>
            {comment.replies?.length > 0 && (
                <div className="children">
                    {comment.replies.map((reply) => (
                        <CommentTree key={reply.id} comment={reply} />
                    ))}
                </div>
            )}
        </div>
    );
};

const CommentDetail = () => {
    const { id: commentId } = useParams();
    const [comment, setComment] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [replyText, setReplyText] = useState('');
    const currentUser = APIService.currentProfile?.username;
    const [isFavorite, setIsFavorite] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchComment = async () => {
            try {
                const response = await APIService.get(`/comments/${commentId}`);
                const commentData = response.data?.comment;
                if (commentData) {
                    setComment(commentData);
                    setIsFavorite(commentData.is_favorite || false);
                } else {
                    setError("Comment not found.");
                }
            } catch {
                setError("Error loading comment.");
            } finally {
                setIsLoading(false);
            }
        };

        fetchComment();
    }, [commentId]);

    const handleVote = () => {
        if (!comment) return;

        const isVoting = !comment.has_voted;
        const apiCall = isVoting
            ? APIService.post(`/comments/${comment.id}/vote`)
            : APIService.delete(`/comments/${comment.id}/vote`);

        apiCall
            .then(() => {
                setComment((prevState) => ({
                    ...prevState,
                    has_voted: isVoting,
                    points: isVoting ? prevState.points + 1 : prevState.points - 1,
                }));
            })
            .catch((error) => console.error("Error managing vote:", error));
    };

    const handleFavorite = async (e) => {
        e.preventDefault();
        try {
          let response;
          if (isFavorite) {
            response = await APIService.delete(`/comments/${commentId}/favorite`);
            if (response.status === 200) {
              setIsFavorite(false);
            }
          } else {
            response = await APIService.post(`/comments/${commentId}/favorite`);
            if (response.status === 200) {
              setIsFavorite(true);
            }
          }
        } catch (err) {
          console.error('Favorite error:', err);
          if (err.response?.status === 400) {
            // If already in favorites, update UI state
            setIsFavorite(true);
          } else {
            setError(err.response?.data?.detail || err.message);
          }
        }
      };

    const handleReplySubmit = async (e) => {
        e.preventDefault();

        if (!replyText.trim()) return;

        if (comment.author === currentUser) {
            setError("You cannot reply to your own comment.");
            return;
        }

        try {
            const response = await APIService.post(`/comments/${comment.id}/reply`, { text: replyText });

            if (response.status === 201) {
                setReplyText('');  // Limpiar el campo de texto después de enviar
                setComment((prevComment) => ({
                    ...prevComment,
                    replies: [...prevComment.replies, response.data.comment], // Añadir la nueva respuesta
                }));
            } else {
                setError("Error sending reply.");
            }
        } catch (error) {
            setError("Error sending reply.");
        }
    };

    if (isLoading) return <p>Loading comment...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="main-container">
            <div className="container">
                <div className="news-item">
                    <div className="author">
                        {comment.author === currentUser ? (
                            <span
                                className="author-asterisk"
                                style={{ color: "orange", fontSize: "20px" }}
                            >
                                *
                            </span>
                        ) : (
                            <button
                                className={`vote-button ${
                                    comment.has_voted ? "voted" : ""
                                }`}
                                onClick={() => handleVote()}
                            >
                                {comment.has_voted ? "Unvote" : "Vote"}
                            </button>
                        )}
                        <span className="points">{comment.points} points</span>{" "}
                        by{" "}
                        <a href={`/author/${comment.author}/profile`} className="author-link">
                            {comment.author}
                        </a>{" "}|{" "}
                        <a href={`/comment/${comment.id}`}>{comment.time_ago}</a> |{" "}
                        <a href="#" className="action-link" onClick={handleFavorite}>
                            {isFavorite ? "un-favorite" : "favorite"}
                        </a>| on:{" "}
                        <a
                            href={`/submission/${comment.submission_id}`}
                            className="submission-link"
                        >
                            {comment.submission_title}
                        </a>
                        {comment.author === currentUser && (
                            <>
                                {" "}|{" "}
                                <a href={`/comments/${comment.id}/edit`} className="edit-link">
                                    edit
                                </a>{" "} |{" "}
                                <a
                                    href={`/comments/${comment.id}/delete`}
                                    className="delete-link"
                                >
                                    delete
                                </a>
                            </>
                        )}
                    </div>
                    <div className="text">{comment.text}</div>
                    {/* Formulario para responder */}
                    {comment.author !== currentUser && (
                        <div className="reply-form">
                            <form onSubmit={handleReplySubmit}>
                                <textarea
                                    value={replyText}
                                    onChange={(e) => setReplyText(e.target.value)}
                                    placeholder="Write your reply..."
                                    rows="4"
                                    cols="50"
                                    className="reply-textarea"
                                />
                                <button
                                    type="submit"
                                    className="submit-reply-button"
                                    disabled={!replyText.trim()}
                                >
                                    Reply
                                </button>
                            </form>
                        </div>
                    )}
                </div>

                {/* Título de las respuestas */}
                {comment.replies?.length > 0 && (
                    <div className="replies-title">
                        <h3>Replies:</h3>
                    </div>
                )}

                <div className="comment-tree-root">
                    {comment.replies?.map((reply) => (
                        <CommentTree key={reply.id} comment={reply} />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default CommentDetail;
