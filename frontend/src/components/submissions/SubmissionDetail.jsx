import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import APIService from '../../services/ApiService';
import '../../styles/SubmissionDetail.css';
import Header from '../Header';

const SubmissionDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [submission, setSubmission] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAuthor, setIsAuthor] = useState(false);
  const [isVoted, setIsVoted] = useState(false);


  const currentUser = APIService.currentProfile?.username; // Añadir esta línea
  const [isFavorite, setIsFavorite] = useState(false);

  const handleFavorite = async (e) => {
    e.preventDefault();
    try {
      let response;
      if (isFavorite) {
        response = await APIService.delete(`/submission/${id}/favorite`);
        if (response.status === 200) {
          setIsFavorite(false);
        }
      } else {
        response = await APIService.post(`/submission/${id}/favorite`);
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

  useEffect(() => {
    const fetchSubmissionDetails = async () => {
      try {
        setLoading(true);
        const response = await APIService.get(`/submission/${id}`);
        
        if (response.status === 200) {
          setSubmission(response.data.submission);
          setComments(response.data.comments || []);
          setIsFavorite(response.data.submission.is_favorite || false);
          setIsVoted(response.data.submission.has_voted || false);
          const currentUser = APIService.currentProfile?.username;
          setIsAuthor(currentUser === response.data.submission.author);
        } else {
          throw new Error('No submission data found');
        }
      } catch (err) {
        console.error('Error fetching data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchSubmissionDetails();
    }
  }, [id]);

  const handleVoteComment = async (id) => {
    if (!comments || comments.length === 0) {
        console.error("Comments array is undefined or empty");
        return;
    }

    const comment = comments.find(comment => comment.id === id);
    if (!comment) {
        console.error(`Comment with id ${id} not found`);
        return;
    }

    const isVoting = !comment.has_voted;
    const apiUrl = `/comments/${id}/vote`;

    try {
        if (isVoting) {
            await APIService.post(apiUrl);
        } else {
            await APIService.delete(apiUrl);
        }

        // Actualizar el estado de los comentarios
        setComments(prevComments =>
            prevComments.map(c =>
                c.id === id
                    ? { ...c, has_voted: !c.has_voted, points: c.points + (isVoting ? 1 : -1) }
                    : c
            )
        );
    } catch (error) {
        console.error('Error al votar el comentario:', error);
    }
};

const handleVote = async (e) => {
  e.preventDefault();
  try {
    let response;
    if (isVoted) {
      response = await APIService.delete(`/submission/${id}/vote`);
      if (response.status === 200) {
        setIsVoted(false);
        setSubmission(prev => ({
          ...prev,
          points: prev.points - 1,
          has_voted: false
        }));
      }
    } else {
      response = await APIService.post(`/submission/${id}/vote`);
      if (response.status === 200) {
        setIsVoted(true);
        setSubmission(prev => ({
          ...prev,
          points: prev.points + 1,
          has_voted: true
        }));
      }
    }
  } catch (err) {
    console.error('Vote error:', err);
    if (err.response?.status === 400) {
      setIsVoted(true);
    } else {
      setError(err.response?.data?.detail || err.message);
    }
  }
};
  const handleDelete = async () => {
    try {
      await APIService.delete(`/submission/${id}`);
      navigate('/');
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!submission) return <div>No submission found</div>;

  return (
    <div className="main-container">
        <Header />
        {loading ? (
            <div className="loading">Loading...</div>
        ) : error ? (
            <div className="error">{error}</div>
        ) : (
            <div className="submission-container">
                <div className="submission-header">
                    {submission.author === currentUser ? (
                        <span className="author-asterisk">*</span>
                    ) : (
                      <button
                        className={`vote-button ${
                            isVoted ? "voted" : ""
                        }`}
                        onClick={handleVote}
                    >
                        {isVoted ? "Unvote" : "Vote"}
                    </button>
                    )}
                    <h1 className="submission-title">{submission.title}</h1>
                </div>
                
                {submission.url && (
                    <div className="submission-url">
                        <a href={submission.url} target="_blank" rel="noopener noreferrer">
                            {submission.shortened_url}
                        </a>
                    </div>
                )}
                
                {submission.text && (
                    <div className="submission-text">{submission.text}</div>
                )}
                
                <div className="submission-info">
                    {submission.points} points by{" "}
                    {submission.author === currentUser ? (
                        <a href="/profile" className="author-link">
                            <b>{submission.author}</b>
                        </a>
                    ) : (
                        <a href={`/author/${submission.author}/profile`} className="author-link">
                            {submission.author}
                        </a>
                    )}{" "}
                    | {submission.time_ago} |{" "}
                    <a href="#" className="action-link" onClick={handleFavorite}>
                        {isFavorite ? "un-favorite" : "favorite"}
                    </a>
                    {isAuthor && (
                        <>
                            <span className="separator">|</span>
                            <a href={`/submissionedit/${submission.id}`} className="action-link">
                                edit
                            </a>
                            <span className="separator">|</span>
                            <a href="#" className="action-link" onClick={handleDelete}>
                                delete
                            </a>
                        </>
                    )}
                </div>

                <div className="comments-section">
                  <h2 className="comments-title">Comments</h2>
                  {comments.map(comment => (
                      <div key={comment.id} className="comment">
                          <div className="news-content">
                              {comment.author !== currentUser && (
                                  <button
                                      className={`vote-button ${comment.has_voted ? "voted" : ""}`}
                                      onClick={() => handleVoteComment(comment.id)}
                                  >
                                      {comment.has_voted ? "unvote" : "vote"}
                                  </button>
                              )}
                              <div className="comment-content">
                                  <div className="comment-header">
                                      <span className="points">{comment.points} points</span>
                                      {" by "}
                                      {comment.author === currentUser ? (
                                          <a href="/profile" className="author-link">
                                              <b>{comment.author}</b>
                                          </a>
                                      ) : (
                                          <a href={`/author/${comment.author}/profile`} className="author-link">
                                              {comment.author}
                                          </a>
                                      )}
                                      {" | "}
                                      <a href={`/comment/${comment.id}`} className="time-ago">
                                          {comment.time_ago}
                                      </a>
                                      {" | "}
                                      <a href="#" className="action-link" onClick={() => handleReply(comment.id)}>
                                          reply
                                      </a>
                                      {/* Resto de acciones */}
                                  </div>
                                  <div className="comment-text">{comment.text}</div>
                              </div>
                          </div>
                          {/* Sección de respuestas con la misma estructura */}
                      </div>
                  ))}
              </div>
            </div>
        )}
    </div>
  );
};

export default SubmissionDetail;