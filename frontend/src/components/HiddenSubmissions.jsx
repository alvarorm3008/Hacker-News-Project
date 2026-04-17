import React, { Component } from "react";
import APIService from "../services/ApiService";
import "../styles/News.css"; // Importamos el CSS

class HiddenSubmissions extends Component {
    constructor(props) {
        super(props);
        this.state = {
            hiddenSubmissions: [],
            loading: true,
            error: null,
        };
    }

    // Llamada a la API para obtener las hidden submissions
    componentDidMount() {
        APIService.get("/hidden_submissions") 
            .then((response) => {
                this.setState({
                    hiddenSubmissions: response.data,
                    loading: false,
                });
            })
            .catch((error) => {
                this.setState({
                    error: "Error loading hidden submissions",
                    loading: false,
                });
            });
    }

    // Manejador de unhide submission
    handleUnhide = (id) => {
        APIService.delete(`/submission/${id}/hide`) // Llamada POST para desocultar
            .then(() => {
                this.setState((prevState) => ({
                    hiddenSubmissions: prevState.hiddenSubmissions.filter(
                        (submission) => submission.id !== id
                    ),
                }));
            })
            .catch((error) => {
                this.setState({
                    error: "Error un-hiding submission",
                });
            });
    };

    render() {
        const { hiddenSubmissions, loading, error } = this.state;
        const currentUser = APIService.currentProfile?.username;
        
        if (loading) {
            return <p className="loading">Loading...</p>;
        }

        if (error) {
            return <p className="error">{error}</p>;
        }

        return (
            <div className="submissions-container">
                {hiddenSubmissions.map((submission) => (
                    <div key={submission.id} className="container">
                        <div className="news-item">
                            {/* Contenedor principal con display flex */}
                            <div className="news-content">
                                {submission.author === currentUser ? (
                                    <span className="author-asterisk" style={{ color: "orange", fontSize: "20px" }}>*</span> // Asterisco naranja
                                ) : (
                                    <button
                                        className={`vote-button ${
                                            submission.has_voted ? "voted" : ""
                                        }`}
                                        onClick={() => this.handleVote(submission.id)}
                                    >
                                        {submission.has_voted ? "Unvote" : "Vote"}
                                    </button>
                                )}
                                <div className="title-container">
                                    {submission.submission_type === "url" && (
                                        <>
                                        <a
                                            href={submission.url}
                                            className="news-title"
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            {submission.title}
                                        </a>
                                        {submission.shortened_url && (
                                            <span className="shortened-url">
                                            (
                                            <a
                                                href={submission.url}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                            >
                                                {submission.shortened_url}
                                            </a>
                                            )
                                            </span>
                                        )}
                                        </>
                                    )}
                                    {submission.submission_type === "ask" && (
                                        <span className="news-title">{submission.title}</span>
                                    )}
                                    </div>
                            </div>
                            {/* Información adicional */}
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
                                    |{" "}
                                    <a href={`/submission/${submission.id}`}>
                                        {submission.time_ago}
                                    </a>{" "}
                                    |{" "}
                                    <a
                                        href="#"
                                        className="hide-link"
                                        onClick={(e) => {
                                            e.preventDefault(); // Prevenir el comportamiento por defecto del enlace
                                            this.handleUnhide(submission.id);
                                        }}
                                    >
                                        un-hide
                                    </a> |{" "}
                                    {submission.author === currentUser ? (
                                        <>
                                            <a href={`/submissionedit/${submission.id}`} className="author-link">
                                                edit
                                            </a>
                                        </>
                                    ) : (
                                        <a href={`/submission/${submission.id}`}>{submission.num_comments}</a>
                                    )}
                                </span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }
}

export default HiddenSubmissions;
