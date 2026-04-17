import React from 'react';

function NewsItem({ submission }) {
    return (
        <div className="news-item">
            {submission.author ? (
                <span className="orange-asterisk">*</span>
            ) : (
                <button className="vote-button">Vote</button>
            )}
            <a href={submission.url || `/submission/${submission.id}`}>
                {submission.title}
            </a>
            {submission.shortened_url && (
                <a href={submission.url}>({submission.shortened_url})</a>
            )}
            <div className="author">
                <span className="points">{submission.points} points</span> by{' '}
                <a href={`/profile/${submission.author.username}`}>
                    {submission.author.username}
                </a>
                <span className="time">{submission.time_ago}</span>
            </div>
            <div className="text">{submission.text}</div>
        </div>
    );
}

export default NewsItem;