import React, { useState } from "react";

export default function App() {
  const [title, setTitle] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    setResult(null);

    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title })
    });

    const data = await response.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        
        <h1 style={styles.title}>🎬 Movie Genre Predictor</h1>
        <p style={styles.subtitle}>Enter a movie title and get its predicted genre instantly</p>

        <input
          type="text"
          placeholder="Type movie title..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={styles.input}
        />

        <button onClick={handlePredict} style={styles.button}>
          {loading ? "Predicting..." : "Predict Genre"}
        </button>

        {result && (
          <div style={styles.resultBox}>
            <p style={styles.resultText}><strong>🎞 Title:</strong> {result.title}</p>
            <p style={styles.resultText}><strong>⭐ Predicted Genre:</strong> {result.predicted_genre}</p>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "linear-gradient(135deg, #4a27ff, #8a5cff, #c59dff)",
    padding: "20px",
  },

  card: {
    width: "100%",
    maxWidth: "500px",
    padding: "30px",
    borderRadius: "18px",
    background: "rgba(255, 255, 255, 0.15)",
    backdropFilter: "blur(12px)",
    border: "1px solid rgba(255, 255, 255, 0.2)",
    textAlign: "center",
    boxShadow: "0 8px 25px rgba(0,0,0,0.2)",
  },

  title: {
    fontSize: "28px",
    fontWeight: "bold",
    color: "#fff",
    marginBottom: "10px",
  },

  subtitle: {
    fontSize: "15px",
    color: "#f0e6ff",
    marginBottom: "20px",
  },

  input: {
    width: "90%",
    padding: "14px",
    fontSize: "16px",
    borderRadius: "10px",
    marginBottom: "18px",
    border: "none",
    outline: "none",
    background: "rgba(255,255,255,0.8)",
  },

  button: {
    width: "90%",
    padding: "14px",
    fontSize: "17px",
    fontWeight: "600",
    background: "#ffffff",
    color: "#4a27ff",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    transition: "0.3s",
  },

  resultBox: {
    marginTop: "25px",
    padding: "20px",
    borderRadius: "14px",
    background: "rgba(255,255,255,0.2)",
    border: "1px solid rgba(255,255,255,0.3)",
    backdropFilter: "blur(10px)",
  },

  resultText: {
    fontSize: "17px",
    color: "#fff",
    marginBottom: "8px",
  }
};
