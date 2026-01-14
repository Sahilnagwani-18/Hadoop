import { useState } from "react";

export default function MovieDashboard() {
  const [movie, setMovie] = useState("");
  const [stats, setStats] = useState(null);
  const [dist, setDist] = useState([]);
  const [similar, setSimilar] = useState([]);

  const load = async () => {
    const s = await fetch(`/movie/${movie}/stats`).then(r=>r.json());
    const d = await fetch(`/movie/${movie}/rating_distribution`).then(r=>r.json());
    const sim = await fetch(`/movie/${movie}/similar`).then(r=>r.json());

    setStats(s);
    setDist(d);
    setSimilar(sim);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Movie Dashboard</h1>

      <input value={movie} onChange={(e)=>setMovie(e.target.value)} />
      <button onClick={load}>Search</button>

      {stats && (
        <>
          <h2>{stats.movie_name}</h2>
          <p>Total Views: {stats.views}</p>
          <p>Avg Rating: {stats.avg_rating.toFixed(2)}</p>
        </>
      )}

      <h2>Rating Distribution</h2>
      {dist.map((d,i)=> 
        <p key={i}>⭐ {d.rating} — {d.count} votes</p>
      )}

      <h2>Similar Movies</h2>
      {similar.map((m,i)=> <p key={i}>{m.movie_name}</p>)}
    </div>
  );
}
