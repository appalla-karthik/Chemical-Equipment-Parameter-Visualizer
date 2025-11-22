import React, { useState } from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function App() {
  const [file, setFile] = useState(null);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [uploadStatus, setUploadStatus] = useState("");
  const [datasets, setDatasets] = useState([]);
  const [expandedId, setExpandedId] = useState(null);
  const [summaries, setSummaries] = useState({});

  const API = "http://127.0.0.1:8000/api";

  // Load history
  const loadHistory = async () => {
    try {
      const resp = await fetch(`${API}/datasets/`, {
        headers: { Authorization: "Basic " + btoa(username + ":" + password) },
      });

      if (!resp.ok) return alert("Invalid username or password");

      setDatasets(await resp.json());
    } catch (e) {
      alert("Error: " + e.message);
    }
  };

  // Upload CSV
  const uploadCSV = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please select a CSV file");

    setUploadStatus("Uploading...");
    const fd = new FormData();
    fd.append("file", file);

    const resp = await fetch(`${API}/upload/`, {
      method: "POST",
      body: fd,
      headers: { Authorization: "Basic " + btoa(username + ":" + password) },
    });

    if (resp.ok) {
      setUploadStatus("File uploaded successfully");
      loadHistory();
    } else {
      setUploadStatus("Upload failed");
    }
  };

  // Expand history item and fetch summary
  const toggleExpand = async (ds) => {
    // Collapse if clicked same item
    if (expandedId === ds.id) {
      setExpandedId(null);
      return;
    }

    setExpandedId(ds.id);

    // Fetch summary ONLY once
    if (!summaries[ds.id]) {
      const resp = await fetch(`${API}/datasets/${ds.id}/summary/`, {
        headers: { Authorization: "Basic " + btoa(username + ":" + password) },
      });

      if (resp.ok) {
        const summaryData = await resp.json();
        setSummaries((prev) => ({ ...prev, [ds.id]: summaryData }));
      }
    }
  };

  return (
    <div
      style={{
        padding: "30px",
        fontFamily: "Inter, sans-serif",
        minHeight: "100vh",
        background: "#f4f6f9",
      }}
    >
      {/* HEADER */}
      <div style={headerCard}>
        <h1 style={{ margin: 0, color: "#1b3a57" }}>
          Chemical Equipment Visualizer
        </h1>
        <p style={{ marginTop: 6, color: "#5f7a94" }}>
          Upload CSV files and analyze chemical equipment data
        </p>
      </div>

      {/* UPLOAD CARD */}
      <div style={panel}>
        <h2 style={panelTitle}>Upload CSV</h2>

        <div style={{ display: "flex", gap: 15 }}>
          <input
            placeholder="Username"
            style={input}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            placeholder="Password"
            type="password"
            style={input}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
          style={{ marginTop: 15 }}
        />

        <button style={primaryButton} onClick={uploadCSV}>
          Upload File
        </button>

        <p style={{ marginTop: 10, color: "#1a73e8", fontWeight: 600 }}>
          {uploadStatus}
        </p>
      </div>

      {/* HISTORY */}
      <div style={panel}>
        <h2 style={panelTitle}>Upload History</h2>

        <button style={secondaryButton} onClick={loadHistory}>
          Refresh History
        </button>

        <div style={{ marginTop: 15 }}>
          {datasets.map((ds) => (
            <div key={ds.id}>
              <div
                style={{
                  padding: 16,
                  borderRadius: 12,
                  background:
                    expandedId === ds.id ? "#e4ecf7" : "#ffffff",
                  border: "1px solid #d9e2ee",
                  marginTop: 12,
                  cursor: "pointer",
                  transition: "0.2s",
                  boxShadow:
                    expandedId === ds.id
                      ? "0 4px 12px rgba(0,0,0,0.1)"
                      : "0 2px 6px rgba(0,0,0,0.05)",
                }}
                onClick={() => toggleExpand(ds)}
              >
                <strong style={{ fontSize: 16, color: "#1b3a57" }}>
                  {ds.original_filename}
                </strong>
                <br />
                <span style={{ fontSize: 13, color: "#5b6f83" }}>
                  {new Date(ds.uploaded_at).toLocaleString()}
                </span>
              </div>

              {/* EXPANDED ANALYTICS BELOW ITEM */}
              {expandedId === ds.id && summaries[ds.id] && (
                <div style={expandPanel}>
                  <h3 style={{ margin: "5px 0", color: "#1b3a57" }}>
                    Analytics
                  </h3>

                  <p style={{ margin: "4px 0" }}>
                    <strong>Total Equipment:</strong>{" "}
                    {summaries[ds.id].total_count}
                  </p>

                  {/* Chart */}
                  <div style={{ height: 280, marginTop: 15 }}>
                    <Bar
                      data={{
                        labels: Object.keys(
                          summaries[ds.id].type_distribution
                        ),
                        datasets: [
                          {
                            label: "Count",
                            data: Object.values(
                              summaries[ds.id].type_distribution
                            ),
                            backgroundColor: "rgba(0,122,255,0.8)",
                            borderRadius: 8,
                          },
                        ],
                      }}
                    />
                  </div>

                  {/* PDF Button */}
                  <a
                    href={ds.pdf_report}
                    target="_blank"
                    rel="noreferrer"
                    style={pdfButton}
                  >
                    View PDF Report
                  </a>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ---------------- STYLES ---------------- */

const headerCard = {
  background: "#ffffff",
  padding: 25,
  borderRadius: 16,
  marginBottom: 30,
  boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
};

const panel = {
  background: "#ffffff",
  padding: 25,
  borderRadius: 16,
  marginBottom: 30,
  boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
};

const panelTitle = {
  marginTop: 0,
  color: "#1b3a57",
  marginBottom: 15,
};

const input = {
  flex: 1,
  padding: "12px 15px",
  borderRadius: 10,
  border: "1.8px solid #c7d4e6",
  outline: "none",
  fontSize: 15,
  transition: "0.2s",
  background: "#fafbff",
};

const primaryButton = {
  marginTop: 15,
  padding: "12px 22px",
  background: "#1a73e8",
  color: "#fff",
  fontSize: 15,
  borderRadius: 10,
  border: "none",
  cursor: "pointer",
  fontWeight: 600,
};

const secondaryButton = {
  padding: "10px 18px",
  background: "#4b7bd8",
  color: "#fff",
  borderRadius: 10,
  border: "none",
  cursor: "pointer",
  fontWeight: 600,
  marginBottom: 10,
};

const expandPanel = {
  marginTop: 10,
  padding: 20,
  background: "#f7faff",
  borderRadius: 12,
  border: "1px solid #dce7f7",
};

const pdfButton = {
  display: "inline-block",
  marginTop: 15,
  padding: "10px 18px",
  background: "#1b3a57",
  color: "#fff",
  borderRadius: 8,
  textDecoration: "none",
  fontWeight: 600,
};
