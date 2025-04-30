import React from "react";
import "./Dashboard.css";

const parks = [
  "Yellowstone National Park",
  "Yosemite National Park",
  "Grand Canyon National Park",
  "Great Smoky Mountains National Park",
  "Zion National Park",
  "Acadia National Park",
  "Everglades National Park",
  "Rocky Mountain National Park",
];

function Dashboard({ onSelectPark, statusMap }) {
    return (
      <div className="dashboard-wrapper">
        <div className="dashboard-header">WEATHER STATION SYSTEM</div>
  
        <div className="summary-bar">
          <div className="summary-item">
            <div className="status-indicator"></div>
            <span style={{ fontWeight: "bold", color: "#000", marginLeft: "30px" }}>
              System Status:
            </span>
            <span className="live-text pulsing-text" style={{ color: "green", marginRight: "50px" }}>
              LIVE
            </span>
          </div>
  
          <div className="ticker-wrapper">
            <div className="ticker">
              <p>Yellowstone sensor online · Zion temperature stable · Grand Canyon pressure reading updated · Great Smoky Mountains transmitting normally · Rocky Mountain humidity high · Acadia connection stable · Everglades temperature peak expected · 
Yellowstone battery health optimal · Yosemite humidity stable · Grand Canyon sensor recalibration complete · Great Smoky Mountains slight pressure drop detected · Zion sensor ping successful · 
Acadia maintenance check passed · Everglades transmission clear · Rocky Mountain minor latency in data retrieval · Yellowstone temperature forecast updated · Yosemite low humidity warning · 
Grand Canyon wind speed stable · Great Smoky Mountains system uptime: 99.9% · Zion temperature spike monitored · Acadia data archive complete · Everglades high humidity alert cleared · Rocky Mountain temperature consistent · 
Yellowstone satellite link verified · Yosemite temperature expected to rise · Grand Canyon humidity drop expected · Great Smoky Mountains nighttime temperature drop · Zion strong winds expected overnight · Acadia all sensors green · 
Everglades minor delay in pressure readings · Rocky Mountain precipitation chance 20% · Yellowstone expected clear skies · Yosemite RF transmission stable · Grand Canyon battery backup tested</p>
            </div>
          </div>

        </div>
  
        <div className="dashboard-grid">
          {parks.map((park) => (
            <div className="card" key={park} onClick={() => onSelectPark(park)}>
              <img src={`/maps/${getImageFileName(park)}`} alt={park} />
              <div className="card-info">
                <h3>{park}</h3>
                <p className={`sensor-status ${statusMap[park] || "unknown"}`}>
                  STATUS: {statusMap[park] ? statusMap[park].toUpperCase() : "UNKNOWN"}
                </p>
                <div className="open-arrow">&rarr;</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }
  

function getImageFileName(parkName) {
  switch (parkName) {
    case "Yellowstone National Park":
      return "yellowstone.jpg";
    case "Yosemite National Park":
      return "yosemite.jpg";
    case "Grand Canyon National Park":
      return "grandcanyon.jpg";
    case "Great Smoky Mountains National Park":
      return "greatsmoky.jpg"; 
    case "Zion National Park":
      return "zion.jpg";
    case "Acadia National Park":
      return "acadia.jpg";
    case "Everglades National Park":
      return "everglades.jpg";
    case "Rocky Mountain National Park":
      return "rockymountain.jpg";
    default:
      return "placeholder.jpg";
  }
}


export default Dashboard;
