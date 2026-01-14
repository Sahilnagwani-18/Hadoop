import { useState } from "react";
import UserDashboard from "./Dashboard/UserDashboard";
import MovieDashboard from "./Dashboard/MovieDashboard";
import GlobalDashboard from "./Dashboard/GlobalDashboard";
import "./App.css";

export default function App() {
  const [page, setPage] = useState("home");

  return (
    <div style={{ padding: 20 }}>
      <h1 style={{ textAlign: "center" }}>🎬 Hive Movie Analytics Dashboard</h1>

      <div style={{ display: "flex", gap: 10, justifyContent: "center", marginBottom: 20 }}>
        <button onClick={() => setPage("user")}>User Dashboard</button>
        <button onClick={() => setPage("movie")}>Movie Dashboard</button>
        <button onClick={() => setPage("global")}>Global Dashboard</button>
      </div>

      {page === "home" && (
        <p style={{ textAlign: "center", color: "#777" }}>
          Select a dashboard to get started.
        </p>
      )}

      {page === "user" && <UserDashboard />}
      {page === "movie" && <MovieDashboard />}
      {page === "global" && <GlobalDashboard />}
    </div>
  );
}
