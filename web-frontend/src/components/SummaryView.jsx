import React, { useEffect, useState } from "react";
import ChartPanel from "./ChartPanel";
import "./SummaryView.css";

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
    <div className="summary-container">
      <h2 className="summary-title">📊 Uploaded Dataset History</h2>

      <div className="auth-section">
        <input
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="auth-input"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="auth-input"
        />

        <button onClick={fetchHistory} className="auth-button">
          {loading ? "Loading..." : "Load History"}
        </button>
      </div>

      {error && <p className="error-message">❌ {error}</p>}

      {datasets.length === 0 && !loading && (
        <p className="no-data-message">
          📁 No datasets found. Upload from Web or Desktop.
        </p>
      )}

      <div className="datasets-grid">
        {datasets.map((ds) => (
          <DatasetDisplay
            key={ds.id}
            ds={ds}
            username={username}
            password={password}
          />
        ))}
      </div>
    </div>
  );
}

function DatasetDisplay({ ds, username, password }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showPdfModal, setShowPdfModal] = useState(false);

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
    <>
      <div className="dataset-card">
        <div className="dataset-header">
          <h3 className="dataset-filename">{ds.original_filename}</h3>
          <p className="dataset-timestamp">
            {new Date(ds.uploaded_at).toLocaleString()}
          </p>
        </div>

        {loading && <div className="loading-spinner">Loading summary...</div>}

        {!loading && summary && (
          <>
            <div className="summary-stats">
              <div className="stat-item">
                <span className="stat-label">📦 Total Equipment:</span>
                <span className="stat-value">{summary.total_count}</span>
              </div>

              {Object.entries(summary.averages || {}).map(
                ([key, value]) =>
                  value !== null && (
                    <div key={key} className="stat-item">
                      <span className="stat-label">Avg {key}:</span>
                      <span className="stat-value">{value.toFixed(3)}</span>
                    </div>
                  )
              )}
            </div>

            <div className="chart-section">
              <h4 className="chart-title">Type Distribution</h4>
              <ChartPanel summary={summary} />
            </div>

            <div className="actions-section">
              <button
                onClick={() => setShowPdfModal(true)}
                className="pdf-button"
              >
                📄 View PDF Report
              </button>

              <details className="raw-json-details">
                <summary className="json-summary">Show Raw Summary JSON</summary>
                <pre className="json-content">
                  {JSON.stringify(summary, null, 2)}
                </pre>
              </details>
            </div>
          </>
        )}
      </div>

      {/* PDF Modal */}
      {showPdfModal && (
        <PdfModal
          pdfUrl={ds.pdf_report}
          fileName={ds.original_filename}
          onClose={() => setShowPdfModal(false)}
        />
      )}
    </>
  );
}

function PdfModal({ pdfUrl, fileName, onClose }) {
  return (
    <div className="pdf-modal-overlay" onClick={onClose}>
      <div className="pdf-modal-container" onClick={(e) => e.stopPropagation()}>
        <div className="pdf-modal-header">
          <h2 className="pdf-modal-title">📄 {fileName}</h2>
          <button className="pdf-modal-close" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="pdf-modal-content">
          <iframe
            src={pdfUrl}
            title={fileName}
            className="pdf-iframe"
          ></iframe>
        </div>

        <div className="pdf-modal-footer">
          <a
            href={pdfUrl}
            download
            className="pdf-download-button"
          >
            ⬇️ Download PDF
          </a>
        </div>
      </div>
    </div>
  );
}

export default SummaryView;
