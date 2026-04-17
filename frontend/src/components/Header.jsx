// Header.jsx
import React, { useState } from "react";
import "../styles/Header.css";

const Header = () => {
  const [searchQuery, setSearchQuery] = useState("");

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`;
    }
  };

  return (
    <header className="header">
      <h1 className="logo">Hacker News</h1>
      <nav className="nav">
        <a href="/" className="link">Home</a>
        <a href="/newest" className="link">New</a>
        <a href="/threads" className="link">Threads</a>
        <a href="/comments" className="link">Comments</a>
        <a href="/ask" className="link">Ask</a>
        <a href="/submission" className="link">Submit</a>
        <a href="/profile" className="link">Profile</a>
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Buscar..."
            className="search-input"
          />
          <button type="submit" className="search-button">🔍</button>
        </form>
      </nav>
    </header>
  );
};

export default Header;