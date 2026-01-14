import { useState, useEffect } from "react";

export default function GlobalDashboard() {
  const [trending, setTrending] = useState([]);
  const [genreTop, setGenreTop] = useState([]);
  const [genreTrend, setGenreTrend] = useState([]);
  const [active, setActive] = useState([]);

  const load = async () => {
    setTrending(await fetch("/global/trending").then(r=>r.json()));
    setGenreTop(await fetch("/global/top10_per_genre").then(r=>r.json()));
    setGenreTrend(await fetch("/global/genre_trend").then(r=>r.json()));
    setActive(await fetch("/global/active_users").then(r=>r.json()));
  };

  useEffect(()=>{ load(); },[]);

  return (
    <div style={{ padding: 20 }}>

      <h1>Global Dashboard</h1>

      <h2>🔥 Trending Today</h2>
      {trending.map((t,i)=> <p key={i}>{t.movie_name} — {t.views} views</p>)}

      <h2>Top 10 Movies per Genre</h2>
      {genreTop.map((t,i)=> 
        <p key={i}>
          {t.genre} — {t.movie_name} ⭐ {t.avg_rating}
        </p>
      )}

      <h2>Genre Trend</h2>
      {genreTrend.map((g,i)=> <p key={i}>{g.genre} — {g.views} views</p>)}

      <h2>Most Active Users</h2>
      {active.map((u,i)=> <p key={i}>User {u.user_id} — {u.actions} actions</p>)}
    </div>
  );
}
