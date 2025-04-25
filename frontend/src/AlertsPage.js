// src/AlertsPage.js
import React, { useEffect, useState } from "react";
import "./AlertsPage.css";

function AlertsPage({ onBack }) {
  const [storedAlerts, setStoredAlerts] = useState([]);

  useEffect(() => {
    const alerts = JSON.parse(localStorage.getItem("alerts")) || [];
    setStoredAlerts(alerts);
  }, []);

  return (
    <div className="alerts-page">
      <h2>⚠️ System Alerts</h2>
      {storedAlerts.length > 0 ? (
        <ul>
          {storedAlerts.map((alert, index) => (
            <li key={index}>
              <strong>{alert.place}</strong> — {alert.message}
              <br />
              <em>Status: {alert.status}</em>
            </li>
          ))}
        </ul>
      ) : (
        <p>✅ All systems normal.</p>
      )}

      <button onClick={onBack}>⬅ Back</button>
    </div>
  );
}

export default AlertsPage;
