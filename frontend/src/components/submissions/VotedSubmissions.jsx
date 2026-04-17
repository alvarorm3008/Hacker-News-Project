// src/components/submissions/VotedSubmissions.jsx
import React, { Component } from "react";
import APIService from "../../services/ApiService";
import "../../styles/News.css";
import Header from "../Header";

class VotedSubmissions extends Component {
    constructor(props) {
        super(props);
        this.state = {
            submissions: [],
            loading: true,
            error: null
        };
    }

    componentDidMount() {
        APIService.get(`/voted_submissions`)
            .then((response) => {
                this.setState({
                    submissions: response.data,
                    loading: false
                });
            })
            .catch((error) => {
                this.setState({
                    error: "Error loading voted submissions",
                    loading: false
                });
            });
    }

    handleVote = (id) => {
        const apiUrl = `/submission/${id}/vote`;
    
        APIService.delete(apiUrl)
            .then((response) => {
                if (response.status === 200) {
                    this.setState((prevState) => ({
                        submissions: prevState.submissions.filter(
                            submission => submission.id !== id
                        )
                    }));
                }
            })
            .catch((error) => {
                console.error("Error removing vote:", error);
                this.setState({ error: "Error removing vote" });
            });
    };

    render() {
        const { submissions, loading, error } = this.state;
        const currentUser = APIService.currentProfile?.username;

        if (loading) return <p className="loading">Loading...</p>;
        if (error) return <p className="error">{error}</p>;

        return (
            <div className="main-container">
                <Header />
                <div className="submissions-container">
                    <h2>Voted Submissions</h2>
                    {submissions.map((submission) => (
                        <div key={submission.id} className="container">
                            <div className="news-item">
                                <div className="news-content">
                                    <button
                                        className={`vote-button ${
                                            submission.has_voted ? "voted" : ""
                                        }`}
                                        onClick={() => this.handleVote(submission.id)}
                                    >
                                        {submission.has_voted ? "Unvote" : "Vote"}
                                    </button>
                                    <div className="title-container">
                                        {submission.submission_type === "url" ? (
                                            <a
                                                href={submission.url}
                                                className="news-title"
                                                target="_blank"
                                                rel="noopener noreferrer"
                                            >
                                                {submission.title}
                                            </a>
                                        ) : (
                                            <a 
                                                href={`/submission/${submission.id}`}
                                                className="news-title"
                                            >
                                                {submission.title}
                                            </a>
                                        )}
                                    </div>
                                </div>
                                <div className="author-points-container">
                                    <span className="points">
                                        {submission.points} points
                                    </span>
                                    <span className="author">
                                        by{" "}
                                        {submission.author === currentUser ? (
                                            <a href="/profile" className="author-link">
                                                <b>{submission.author}</b>
                                            </a>
                                        ) : (
                                            <a href={`/author/${submission.author}/profile`} className="author-link">
                                                {submission.author}
                                            </a>
                                        )}{" "}
                                        | <a href={`/submission/${submission.id}`}>{submission.time_ago}</a>{" "}
                                        | {submission.num_comments}
                                    </span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }
}

export default VotedSubmissions;