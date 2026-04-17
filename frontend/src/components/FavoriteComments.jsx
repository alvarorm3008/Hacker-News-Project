import React, { Component } from "react";
import APIService from "../services/ApiService";
import "../styles/Threads.css"; // Importando el CSS adaptado

class FavoriteComments extends Component {
    constructor(props) {
        super(props);
        this.state = {
            favoriteComments: [],
            loading: true,
            error: null,
        };
    }

    componentDidMount() {
        APIService.get("/favorite_comments")
            .then((response) => {
                this.setState({
                    favoriteComments: response.data,
                    loading: false,
                });
            })
            .catch((error) => {
                this.setState({
                    error: "Error loading favorite comments",
                    loading: false,
                });
            });
    }

    // Manejador de voto simulado
    handleVote = (id) => {
        this.setState((prevState) => ({
            favoriteComments: prevState.favoriteComments.map((comment) =>
                comment.id === id
                    ? { ...comment, has_voted: !comment.has_voted }
                    : comment
            ),
        }));
    };

    // Manejador de unfavorite submission
    handleUnfavorite = (id) => {
        APIService.delete(`/comments/${id}/favorite`) // Llamada delete para desfavorito
            .then(() => {
                this.setState((prevState) => ({
                    favoriteComments: prevState.favoriteComments.filter(
                        (comment) => comment.id !== id
                    ),
                }));
            })
            .catch((error) => {
                this.setState({
                    error: "Error unfavoriting comment",
                });
            });
    };

    render() {
        const { favoriteComments, loading, error } = this.state;
        const currentUser = APIService.currentProfile?.username;


        if (loading) {
            return <p>Loading...</p>;
        }

        if (error) {
            return <p>{error}</p>;
        }

        return (
            <div className="threads-container">
                {/* Contenedor principal */}
                {favoriteComments.length === 0 ? (
                    <div className="comment no-comments">
                        You haven't added any comments to your favorites yet.
                    </div>
                ) : (
                    favoriteComments.map((comment) => (
                        <div key={comment.id} className="comment">
                            <div className="author">
                                
                                {comment.author === currentUser ? (
                                    <span className="author-asterisk" style={{ color: "orange", fontSize: "20px" }}>*</span> // Asterisco naranja
                                ) : (
                                    <button
                                        className={`vote-button ${
                                            comment.has_voted ? "voted" : ""
                                        }`}
                                        onClick={() => this.handleVote(comment.id)}
                                    >
                                        {comment.has_voted ? "Unvote" : "Vote"}
                                    </button>
                                )}

                                <span className="points">{comment.points} points {" "}</span>
                                by {comment.author === currentUser ? (
                                    <a href="/profile" className="author-link">
                                        <b>{comment.author}</b>
                                    </a>
                                ) : (
                                    <a href={`/author/${comment.author}/profile`} className="author-link">
                                        {comment.author}
                                    </a>
                                )}{" "} 
                                |{" "}
                                <a href={`/comment/${comment.id}`}>{comment.time_ago}</a> |{" "}
                                <a
                                    href="#"
                                    className="favorite-link"
                                    onClick={(e) => {
                                        e.preventDefault(); // Prevenir el comportamiento por defecto del enlace
                                        this.handleUnfavorite(comment.id);
                                    }}
                                >
                                    un-favorite
                                </a> |{" "}on:{" "}
                                <a href={`/submission/${comment.submission_id}`}>{comment.submission_title}</a>
                            </div>
                            <div className="text">{comment.text}</div>
                        </div>
                    ))
                )}
            </div>
        );
    }
}

export default FavoriteComments;
