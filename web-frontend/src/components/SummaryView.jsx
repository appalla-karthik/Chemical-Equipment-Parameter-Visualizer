import React, { useEffect, useState } from "react";
import ChartPanel from "./ChartPanel";

function SummaryView() {
  const [datasets, setDatasets] = useState([]);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchHistory = async () => {
    if (!username || !password) {
      setError("Enter username & password first");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const resp = await fetch("http://127.0.0.1:8000/api/datasets/", {
        headers: {
          Authorization: "Basic " + btoa(username + ":" + password),
        },
      });

      if (!resp.ok) {
        throw new Error("Failed to fetch history (wrong credentials?)");
      }

      const data = await resp.json();
      setDatasets(data);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  return (
    <div style={{ marginTop: 30 }}>
      <h2>Uploaded Dataset History</h2>

      <div style={{ marginBottom: 10 }}>
        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{
            padding: 6,
            marginRight: 10,
            borderRadius: 4,
            border: "1px solid #ccc",
          }}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{
            padding: 6,
            marginRight: 10,
            borderRadius: 4,
            border: "1px solid #ccc",
          }}
        />

        <button
          onClick={fetchHistory}
          style={{
            padding: "6px 14px",
            background: "#0057e7",
            color: "#fff",
            border: "none",
            borderRadius: 4,
            cursor: "pointer",
          }}
        >
          Load History
        </button>
      </div>

      {loading && <p>Loading datasets...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {datasets.length === 0 && !loading && (
        <p>No datasets found. Upload from Web or Desktop.</p>
      )}

      {datasets.map((ds) => (
        <DatasetDisplay
          key={ds.id}
          ds={ds}
          username={username}
          password={password}
        />
      ))}
    </div>
  );
}

function DatasetDisplay({ ds, username, password }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch summary when component mounts
  useEffect(() => {
    const loadSummary = async () => {
      try {
        const resp = await fetch(
          `http://127.0.0.1:8000/api/datasets/${ds.id}/summary/`,
          {
            headers: {
              Authorization: "Basic " + btoa(username + ":" + password),
            },
          }
        );

        if (resp.ok) {
          const data = await resp.json();
          setSummary(data);
        }
      } catch (err) {
        console.error("Summary error:", err);
      }

      setLoading(false);
    };

    loadSummary();

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // only once when mounted

  return (
    <div
      style={{
        border: "1px solid #ccc",
        padding: 15,
        marginTop: 20,
        borderRadius: 6,
        background: "#fafafa",
      }}
    >
      <h3 style={{ marginBottom: 5 }}>{ds.original_filename}</h3>
      <p style={{ marginTop: 0, color: "#666" }}>
        Uploaded at: {new Date(ds.uploaded_at).toLocaleString()}
      </p>

      {loading && <p>Loading summary...</p>}
      {!loading && summary && (
        <>
          <p>
            <strong>Total Equipment:</strong> {summary.total_count}
          </p>

          <div style={{ marginTop: 20 }}>
            <h4>Type Distribution Chart</h4>
            <ChartPanel summary={summary} />
          </div>

          <div style={{ marginTop: 10 }}>
            <a
              href={ds.pdf_report}
              target="_blank"
              rel="noreferrer"
              style={{
                textDecoration: "none",
                color: "#0057e7",
                fontWeight: "bold",
              }}
            >
              📄 View PDF Report
            </a>
          </div>

          <details
            style={{
              marginTop: 10,
              cursor: "pointer",
              padding: 6,
              borderRadius: 4,
              background: "#fff",
            }}
          >
            <summary>Raw Summary JSON</summary>
            <pre
              style={{
                background: "#eee",
                padding: 10,
                borderRadius: 6,
                marginTop: 10,
              }}
            >
              {JSON.stringify(summary, null, 2)}
            </pre>
          </details>
        </>
      )}
    </div>
  );
}

export default SummaryView;
