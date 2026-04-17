import React from 'react';

function CommentItem({ comment }) {
    return (
        <li className="comment">
            <p>{comment.text}</p>
            <div className="author">
                <span>{comment.author}</span> | <span>{comment.time_ago}</span>
            </div>
        </li>
    );
}

export default CommentItem;