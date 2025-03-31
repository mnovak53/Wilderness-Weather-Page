import React from "react";
import "./WelcomeScreen.css";

function WelcomeScreen({ onEnter }) {
  return (
    <div className="welcome-container">
      <div className="welcome-content">
        <h1>WELCOME TO YOUR WEATHER SYSTEM</h1>
        <button onClick={onEnter}>Launch Dashboard</button>
      </div>
    </div>
  );
}

export default WelcomeScreen;
