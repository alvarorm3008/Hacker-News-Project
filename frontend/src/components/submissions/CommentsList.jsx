import React from 'react';
import CommentItem from './CommentItem';

function CommentsList({ comments }) {
    if (comments.length === 0) {
        return <p>No comments yet.</p>;
    }

    return (
        <div>
            <h2>Comments</h2>
            <ul>
                {comments.map((comment) => (
                    <CommentItem key={comment.id} comment={comment} />
                ))}
            </ul>
        </div>
    );
}

export default CommentsList;
