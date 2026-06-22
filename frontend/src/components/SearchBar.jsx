import { useState } from "react";

function SearchBar({ onSearch }) {
  const [city, setCity] = useState("Kochi");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!city.trim()) return;

    onSearch(city);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="search-form"
    >
      <input
        type="text"
        placeholder="Enter City"
        value={city}
        onChange={(e) =>
          setCity(e.target.value)
        }
      />

      <button type="submit">
        Analyze
      </button>
    </form>
  );
}

export default SearchBar;
