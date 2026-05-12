import { useState } from "react";

const API = "http://localhost:8000";

export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [collection, setCollection] = useState([]);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    if (!query.trim()) return;
    setLoading(true);
    const res = await fetch(`${API}/search?q=${query}`);
    const data = await res.json();
    setResults(data);
    setLoading(false);
  };

  const importAlbum = async (mbid) => {
    await fetch(`${API}/albums/import?mbid=${mbid}`, { method: "POST" });
    loadCollection();
  };

  const loadCollection = async () => {
    const res = await fetch(`${API}/albums`);
    const data = await res.json();
    setCollection(data);
  };

  return (
    <div style={{ maxWidth: 800, margin: "0 auto", padding: 24, fontFamily: "sans-serif" }}>
      <h1>🎵 MusicShelf</h1>

      <div style={{ display: "flex", gap: 8, marginBottom: 24 }}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === "Enter" && search()}
          placeholder="Cerca un album..."
          style={{ flex: 1, padding: 8, fontSize: 16 }}
        />
        <button onClick={search} style={{ padding: "8px 16px" }}>Cerca</button>
        <button onClick={loadCollection} style={{ padding: "8px 16px" }}>La mia collezione</button>
      </div>

      {loading && <p>Caricamento...</p>}

      {results.length > 0 && (
        <div>
          <h2>Risultati ricerca</h2>
          {results.map(album => (
            <div key={album.mbid} style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 16, borderBottom: "1px solid #eee", paddingBottom: 16 }}>
              <img src={album.cover_url} alt={album.title} width={60} height={60} style={{ objectFit: "cover" }} onError={e => e.target.style.display = "none"} />
              <div style={{ flex: 1 }}>
                <strong>{album.title}</strong>
                <div style={{ color: "#666" }}>{album.artist} — {album.year}</div>
              </div>
              <button onClick={() => importAlbum(album.mbid)}>+ Aggiungi</button>
            </div>
          ))}
        </div>
      )}

      {collection.length > 0 && (
        <div>
          <h2>La mia collezione</h2>
          {collection.map(album => (
            <div key={album.id} style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 16, borderBottom: "1px solid #eee", paddingBottom: 16 }}>
              <img src={album.cover_url} alt={album.title} width={60} height={60} style={{ objectFit: "cover" }} onError={e => e.target.style.display = "none"} />
              <div>
                <strong>{album.title}</strong>
                <div style={{ color: "#666" }}>{album.artists.map(a => a.name).join(", ")} — {album.year}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}