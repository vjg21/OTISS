import { useEffect, useState } from "react";
import "./Tools.css";

const API_BASE = "http://127.0.0.1:8000";

export default function Tools() {
  const [categories, setCategories] = useState({});
  const [activeCategory, setActiveCategory] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/tools`)
      .then((res) => res.json())
      .then((data) => {
        setCategories(data.categories || {});
        const firstCategory = Object.keys(data.categories || {})[0];
        setActiveCategory(firstCategory);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p className="tools-loading">Loading tools...</p>;
  }

  return (
    <div className="tools-page">
     

      {/* CATEGORY BUTTONS */}
      <div className="category-bar">
        {Object.keys(categories).map((cat) => (
          <button
            key={cat}
            className={`category-btn ${
              activeCategory === cat ? "active" : ""
            }`}
            onClick={() => setActiveCategory(cat)}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* TOOLS LIST */}
      <div className="tools-grid">
        {categories[activeCategory]?.map((tool, idx) => (
          <div key={idx} className="tool-card">
            <h3>{tool.name}</h3>
            <p>{tool.description}</p>
            <a
              href={tool.url}
              target="_blank"
              rel="noopener noreferrer"
            >
              Open Tool →
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
