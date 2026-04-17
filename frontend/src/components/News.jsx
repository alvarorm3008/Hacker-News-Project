import React, { Component } from "react";
import { Link } from "react-router-dom";
import APIService from "../services/ApiService";
import "../styles/News.css"; // Importamos el CSS

class News extends Component {
    constructor(props) {
        super(props);
        this.state = {
            submissions: [],
            loading: true,
            error: null,
        };
    }

    // Llamada a la API para obtener las submissions
    componentDidMount() {
        APIService.get("/news") 
            .then((response) => {
                this.setState({
                    submissions: response.data,
                    loading: false,
                });
            })
            .catch((error) => {
                this.setState({
                    error: "Error loading submissions",
                    loading: false,
                });
            });
    }

    // Manejador de voto simulado
    handleVote = (id) => {
            const { submissions } = this.state; // Extreu comments de l'estat
    
            if (!submissions || submissions.length === 0) {
                console.error("Submissions array is undefined or empty");
                return; // Sortim si comments no està definit
            }
    
            const submission = submissions.find((submission) => submission.id === id);
    
            if (!submission) {
                console.error(`Submission with id ${id} not found`);
                return; // Sortim si el comentari no existeix
            }
            console.log(submission.has_voted);
            const apiUrl = `/submission/${id}/vote`;
    
            const apiCall = submission.has_voted
                ? APIService.delete(apiUrl) 
                : APIService.post(apiUrl); 
            console.log(submission.has_voted);

            apiCall
                .then((response) => {
                    if (response.status === 200) {
                    // Actualitza l'estat només si l'API té èxit
                    const updatedSubmission = response.data.submission;
                    console.log('API response submission:', updatedSubmission);
                    console.log(submission.has_voted);

                    this.setState(prevState => ({
                        submissions: prevState.submissions.map(s => 
                            s.id === id ? updatedSubmission : s
                        )
                    })) 
                    console.log(submission.has_voted);  
                 }

                })
                .catch((error) => {
                    console.error("Error managing vote:", error);
                });
    };

    // Manejador de ocultar submission
    handleHide = (id) => {
        APIService.post(`/submission/${id}/hide`) // Llamada POST para ocultar
            .then(() => {
                // Una vez la respuesta sea exitosa, actualizamos el estado
                this.setState((prevState) => ({
                    submissions: prevState.submissions.filter(
                        (submission) => submission.id !== id
                    ),
                }));
            })
            .catch((error) => {
                this.setState({
                    error: "Error hiding submission",
                });
            });
    };

    render() {
        const { submissions, loading, error } = this.state;
        const currentUser = APIService.currentProfile?.username;

        if (loading) {
            return <p className="loading">Loading...</p>;
        }

        if (error) {
            return <p className="error">{error}</p>;
        }

        return (
            <div className="submissions-container">
                {submissions.map((submission) => (
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
                                    <a
                                        href={submission.url}
                                        className="news-title"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        {submission.title}
                                    </a>
                                    <span className="shortened-url">
                                        (<a
                                            href={submission.url}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                        >
                                            {submission.shortened_url}
                                        </a>)
                                    </span>
                                </div>
                            </div>
                            {/* Información adicional */}
                            <div className="author-points-container">
                                <span className="points">
                                    {submission.points} points
                                </span>
                                <span className="author">
                                    {" "}by{" "}
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
                                            this.handleHide(submission.id);
                                        }}
                                    >
                                        hide
                                    </a> |{" "}
                                    {submission.author === currentUser ? (
                                        <>
                                            <a href={`/submissionedit/${submission.id}`} className="author-link">
                                                edit
                                            </a>
                                            {" "}|{" "}
                                            <a href={`/submissiondelete/${submission.id}`} className="author-link">
                                                delete
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

export default News;
