import React, { Component } from "react";
import APIService from "../services/ApiService";
import "../styles/Threads.css"; // Importamos el CSS

class Threads extends Component {
  constructor(props) {
    super(props);
    this.state = {
      comments: [],
      loading: true,
      error: null,
    };
  }

  componentDidMount() {
    APIService.get("/threads")
      .then((response) => {
        this.setState({
          comments: response.data.user_comments || [],
          loading: false,
        });
      })
      .catch((error) => {
        this.setState({
          error: "Error loading threads",
          loading: false,
        });
      });
  }

  // Manejador de vot amb crida a l'API
  handleVote = (id) => {
      const { comments } = this.state; // Extreu comments de l'estat

      if (!comments || comments.length === 0) {
          console.error("Comments array is undefined or empty");
          return; // Sortim si comments no està definit
      }

      const comment = comments.find((comment) => comment.id === id);

      if (!comment) {
          console.error(`Comment with id ${id} not found`);
          return; // Sortim si el comentari no existeix
      }

      const isVoting = !comment.has_voted; // Determina si és vot o unvote
      const apiUrl = `/comments/${id}/vote`;

      const apiCall = isVoting
          ? APIService.post(apiUrl) // Crida POST per votar
          : APIService.delete(apiUrl); // Crida DELETE per treure el vot

      apiCall
          .then(() => {
              // Actualitza l'estat només si l'API té èxit
              this.setState((prevState) => ({
                comments: prevState.comments.map((comment) =>
                      comment.id === id
                          ? {
                                ...comment,
                                has_voted: isVoting,
                                points: isVoting
                                    ? comment.points + 1 // Incrementa punts en votar
                                    : comment.points - 1, // Decrementa punts en treure el vot
                            }
                          : comment
                  ),
              }));
          })
          .catch((error) => {
              console.error("Error managing vote:", error);
          });
  };

  renderComments(comments) {
    const currentUser = APIService.currentProfile?.username;

    return comments.map((comment) => (
      <div key={comment.id} className="comment">
        <div className="author">
          {comment.author === currentUser ? (
            <span
              className="author-asterisk"
              style={{ color: "orange", fontSize: "20px" }}
            >
              *
            </span> // Asterisco naranja
          ) : (
            <button
              className={`vote-button ${comment.has_voted ? "voted" : ""}`}
              onClick={() => this.handleVote(comment.id)}
            >
              {comment.has_voted ? "Unvote" : "Vote"}
            </button>
          )}

          <span className="points">{comment.points} points </span>
          by{" "}
          {comment.author === currentUser ? (
            <a href="/profile" className="author-link">
              <b>{comment.author}</b>
            </a>
          ) : (
            <a href={`/author/${comment.author}/profile`} className="author-link">
              {comment.author}
            </a>
          )}{" "}
          | <a href={`/comment/${comment.id}`}>{comment.time_ago}</a> | on:{" "}
          <a href={`/submission/${comment.submission_id}`}>
            {comment.submission_title}
          </a>{" "}
          {comment.author === currentUser && (
            <span>
              |{" "}
              <a href={`/comments/${comment.id}/edit`} className="author-link">
                edit
              </a>{" "}
              |{" "}
              <a
                href={`/comments/${comment.id}/delete`}
                className="author-link"
              >
                delete
              </a>
            </span>
          )}

          <p className="text">{comment.text}</p>
        </div>
        {comment.replies.length > 0 && (
          <div className="replies">{this.renderComments(comment.replies)}</div>
        )}
      </div>
    ));
  }

  render() {
    const { comments, loading, error } = this.state;

    if (loading) {
      return <p className="loading">Loading...</p>;
    }

    if (error) {
      return <p className="error">{error}</p>;
    }

    return (
      <div className="threads-container">
        {/* Comprobamos si hay comentarios */}
        {comments.length === 0 ? (
          <div className="comment no-comments">There are no threads yet.</div>
        ) : (
          this.renderComments(comments)
        )}
      </div>
    );
  }
}

export default Threads;
