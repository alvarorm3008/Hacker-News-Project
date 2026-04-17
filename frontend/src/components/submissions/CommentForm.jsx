import React, { useState } from 'react';

function CommentForm({ submissionId, setComments }) {
    const [text, setText] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        // Simular envío del comentario
        const newComment = {
            id: Date.now(),
            text,
            author: 'Current User',
            time_ago: 'just now',
        };
        setComments((prev) => [...prev, newComment]);
        setText('');
    };

    return (
        <div>
            <h2>Add a Comment</h2>
            <form onSubmit={handleSubmit}>
                <textarea
                    rows="4"
                    cols="50"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Write your comment..."
                />
                <button type="submit">Add Comment</button>
            </form>
        </div>
    );
}

export default CommentForm;