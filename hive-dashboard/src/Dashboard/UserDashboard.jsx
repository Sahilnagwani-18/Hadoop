import { useState } from "react";

export default function UserDashboard() {
  const [uid, setUid] = useState("");
  const [top10, setTop10] = useState([]);
  const [genres, setGenres] = useState([]);
  const [count, setCount] = useState(0);
  const [recent, setRecent] = useState([]);

  const load = async () => {
    const t10 = await fetch(`/user/top10/${uid}`).then(r => r.json());
    const g = await fetch(`/user/genres/${uid}`).then(r => r.json());
    const c = await fetch(`/user/count/${uid}`).then(r => r.json());
    const r20 = await fetch(`/user/recent/${uid}`).then(r => r.json());

    setTop10(t10);
    setGenres(g);
    setCount(c.total);
    setRecent(r20);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>User Dashboard</h1>

      <input value={uid} onChange={(e)=>setUid(e.target.value)} placeholder="Enter User ID" />
      <button onClick={load}>Load</button>

      <h2>Top 10 Rated Movies</h2>
      {top10.map((x,i)=> <p key={i}>{x.movie_name} ⭐ {x.rating}</p>)}

      <h2>Most Watched Genres</h2>
      {genres.map((x,i)=> <p key={i}>{x.genre} — {x.count} views</p>)}

      <h2>Total Movies Watched: {count}</h2>

      <h2>Last 20 Rated</h2>
      {recent.map((x,i)=> <p key={i}>{x.movie_name} ⭐ {x.rating}</p>)}
    </div>
  );
}
