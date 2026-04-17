import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import APIService from '../../services/ApiService';
import '../../styles/FavoriteSubmission.css';

const FavoriteSubmission = () => {
  const { username } = useParams();
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refresh, setRefresh] = useState(0);


  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        console.log('Fetching favorites for username:', username); // Debug log
        const response = await APIService.get(`/author/${username}/favorite_submissions`);
        console.log('Full API Response:', response); // Debug full response
        console.log('Response status:', response.status);
        console.log('Response data:', response.data);
        
        if (response.status === 200) {
          if (Array.isArray(response.data)) {
            setSubmissions(response.data);
            console.log('Set submissions:', response.data);
          } else {
            console.error('Data is not an array:', response.data);
            setSubmissions([]);
          }
        }
      } catch (err) {
        console.error('Error fetching favorites:', err);
        console.error('Error details:', err.response);
        setError(err.response?.status === 404 ? 'Author not found' : err.message);
      } finally {
        setLoading(false);
      }
    };

    if (username) {
      fetchFavorites();
    }
  }, [username, refresh]);

  const handleUnfavorite = async (e, submissionId) => {
    e.preventDefault();
    try {
      const response = await APIService.delete(`/submission/${submissionId}/favorite`);
      if (response.status === 200) {
        setRefresh(prev => prev + 1);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (submissionId) => {
    try {
      await APIService.delete(`/submission/${submissionId}`);
      setRefresh(prev => prev + 1); // Refresh list after delete
    } catch (err) {
      setError(err.message);
    }
  };
  

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="main-container">
      {submissions.length > 0 ? (
        submissions.map(submission => (
          <div key={submission.id} className="container">
            <div className="news-item">
              <span className="orange-asterisk">*</span>
              <Link to={`/submission/${submission.id}`}>{submission.title}</Link>
              {submission.shortened_url && (
                <a href={submission.url}>({submission.shortened_url})</a>
              )}
              <div className="author">
                <span className="points">{submission.points} points</span> by{' '}
                {submission.author === APIService.currentProfile?.username ? (
                <Link to="/profile">{submission.author}</Link>
                ) : (
                <Link to={`/author/${submission.author}/profile`}>{submission.author}</Link>
                )} on{' '}
                <Link to={`/submission/${submission.id}`}>{submission.time_ago}</Link> |{' '}
                <a href="#" onClick={(e) => handleUnfavorite(e, submission.id)}>un-favorite</a>
                {submission.author === APIService.currentProfile?.username && (
                  <>
                    {' | '}
                    <Link to={`/submissionedit/${submission.id}`}>edit</Link>
                    {' | '}
                    <a href="#" onClick={(e) => {
                        e.preventDefault();
                        handleDelete(submission.id);
                    }}>delete</a>                  </>
                )}
              </div>
            </div>
          </div>
        ))
    ) : (
        <div className="news-item no-submissions">
          You haven't added any submissions to your favorites yet.
        </div>
      )}
    </div>
  );
};


export default FavoriteSubmission;