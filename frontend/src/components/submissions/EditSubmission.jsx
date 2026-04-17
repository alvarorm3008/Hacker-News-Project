import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import APIService from '../../services/ApiService';

const EditSubmission = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    text: ''
  });
  const [submission, setSubmission] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSubmission = async () => {
      try {
        const response = await APIService.get(`/submission/${id}`);
        if (response.status === 200) {
          setSubmission(response.data.submission);
          setFormData({
            title: response.data.submission.title,
            text: response.data.submission.text || ''
          });
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSubmission();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await APIService.put(`/submission/${id}`, formData);
      if (response.status === 200) {
        navigate(`/submission/${id}`);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!submission) return <div>Submission not found</div>;

  return (
    <div className="main-container">
      <div className="container">
        <div className="news-item">
          <span className="orange-asterisk">*</span>
          {submission.url ? (
            <a href={submission.url}>{submission.title}</a>
          ) : (
            <a href={`/submission/${submission.id}`}>{submission.title}</a>
          )}
          {submission.shortened_url && (
            <a href={submission.url}>({submission.shortened_url})</a>
          )}
          <div className="author">
            <span className="points">{submission.points} points</span>
            by <span>{submission.author}</span> | 
            <span>{submission.time_ago}</span>
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Title:</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
            />
          </div>
          {submission.url && (
            <div className="form-group">
              <label>URL:</label>
              <p><a href={submission.url} target="_blank" rel="noopener noreferrer">
                {submission.url}
              </a></p>
            </div>
          )}
          <div className="form-group">
            <label htmlFor="text">Text:</label>
            <textarea
              id="text"
              name="text"
              rows="4"
              cols="50"
              value={formData.text}
              onChange={handleChange}
            />
          </div>
          <button type="submit">Update</button>
        </form>
      </div>
    </div>
  );
};

export default EditSubmission;