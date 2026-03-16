import React, { useState } from "react";
import "./SearchBar.css";

interface SearchBarProps {
  onSearch: (query: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch }) => {
  const [query, setQuery] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') onSearch(query);
  };

const handleClear = () => {
  setQuery('');
  onSearch('');
};

  return (
    <div className="search-bar">
      <div className="search-input-wrapper">
        <span className="search-icon">🔍</span>
        <input
          type="text"
          value={query}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder="Search by audio filename..."
          className="search-input"
        />
        {query && (
          <button
            onClick={handleClear}
            className="clear-button"
            aria-label="Clear search"
          >
            ✕
          </button>
        )}
      </div>
      {query && (
        <small className="search-info">
          Searching for: "<em>{query}</em>"
        </small>
      )}
    </div>
  );
};

export default SearchBar;
