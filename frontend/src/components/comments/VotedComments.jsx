import React, { Component } from "react";
import APIService from "../../services/ApiService";
import "../../styles/Threads.css";

class VotedComments extends Component {
    constructor(props) {
        super(props);
        this.state = {
            votedComments: [],
            loading: true,
            error: null,
        };
    }

    componentDidMount() {
        APIService.get("/voted_comments")
            .then((response) => {
                this.setState({
                    votedComments: response.data,
                    loading: false,
                });
            })
            .catch((error) => {
                this.setState({
                    error: "Error loading voted comments",
                    loading: false,
                });
            });
    }

    handleVote = (id) => {
        const apiUrl = `/comments/${id}/vote`;

        APIService.delete(apiUrl)
            .then(() => {
                this.setState((prevState) => ({
                    votedComments: prevState.votedComments.filter(
                        (comment) => comment.id !== id
                    ),
                }));
            })
            .catch((error) => {
                console.error("Error managing vote:", error);
            });
    };

    render() {
        const { votedComments, loading, error } = this.state;

        if (loading) {
            return <p>Loading...</p>;
        }

        if (error) {
            return <p>{error}</p>;
        }

        return (
            <div className="threads-container">
                {votedComments.length === 0 ? (
                    <div className="comment no-comments">
                        You haven&apos;t voted on any comments yet.
                    </div>
                ) : (
                    votedComments.map((comment) => (
                        <div key={comment.id} className="comment">
                            <div className="author">
                                <button
                                    className="vote-button voted"
                                    onClick={() => this.handleVote(comment.id)}
                                >
                                    Unvote
                                </button>
                                <span className="points">{comment.points} points </span>
                                by <a href={`/author/${comment.author}/profile`}>{comment.author}</a> | 
                                <a href={`/comment/${comment.id}`}>{comment.time_ago}</a> | on: {" "}
                                <a href={`/submission/${comment.submission_id}`}>
                                    {comment.submission_title}
                                </a>
                            </div>
                            <div className="text">{comment.text}</div>
                        </div>
                    ))
                )}
            </div>
        );
    }
}

export default VotedComments;
