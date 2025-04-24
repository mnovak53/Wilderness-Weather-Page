//co-author: chat gpt
import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import WelcomeScreen from "./WelcomeScreen";
import AlertsPage from "./AlertsPage";


function App() {
  const [entered, setEntered] = useState(false);
  const [weatherData, setWeatherData] = useState([]);
  const [notification, setNotification] = useState("");
  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState("GOOD");
  const [alerts, setAlerts] = useState([]);

  const [viewingAlerts, setViewingAlerts] = useState(false);

  const [selectedCity, setSelectedCity] = useState("All");
  const cityOptions = [
    "All",
    "Yellowstone National Park",
    "Yosemite National Park",
    "Grand Canyon National Park",
    "Great Smoky Mountains National Park",
    "Zion National Park",
    "Acadia National Park",
    "Everglades National Park",
    "Rocky Mountain National Park"
  ];
  

  const fetchNewData = async () => {
    try {
      setNotification("Fetching and archiving data...");
  
      //fetch new weather + get alerts
      const fetchRes = await axios.post("http://localhost:5000/api/fetch");
      const alerts = fetchRes.data.alerts || [];
      localStorage.setItem("system_alerts", JSON.stringify(alerts));  // ⬅️ Save alerts
  
      //archive new data
      await axios.post("http://localhost:5000/api/archive");
  
      //load latest data
      const res = await axios.get("http://localhost:5000/api/weather");
      setWeatherData(res.data);
  
      setNotification("✅ New weather data fetched and stored.");
      setStatus(alerts.length > 0 ? "REVIEW" : "GOOD"); //show status
    } catch (error) {
      console.error(error);
      setNotification("❌ Failed to fetch data.");
      setStatus("REVIEW");
    }
  };
  
  
  
  

  const getLatestRecords = async () => {
    try {
      setNotification("Loading latest records...");
  
      const url = selectedCity === "All"
        ? "http://localhost:5000/api/weather"
        : `http://localhost:5000/api/weather?place=${encodeURIComponent(selectedCity)}`;
  
      const res = await axios.get(url);
      setWeatherData(res.data);
      setNotification("Showing latest records.");
    } catch (error) {
      console.error(error);
      setNotification("Could not load records.");
      setStatus("REVIEW");
    }
  };
  
  

  const goToAlertsPage = () => {
    setViewingAlerts(true);
  };
  

  if (viewingAlerts) {
    return <AlertsPage onBack={() => setViewingAlerts(false)} alerts={alerts} />;
  }
  
  

  if (!entered) {
    return <WelcomeScreen onEnter={() => setEntered(true)} />;
  }

  return (
    <div className="App">
      <div className="top-bar">
  <div className="title-and-filter">
    <h1 className="dashboard-title">🌤️ Weather Station Dashboard</h1>
    <select
      className="city-select"
      value={selectedCity}
      onChange={(e) => setSelectedCity(e.target.value)}
    >
      {cityOptions.map((city) => (
        <option key={city} value={city}>{city}</option>
      ))}
    </select>
  </div>

  <button className="alert-button" onClick={goToAlertsPage}>
    🚨 View Alerts
  </button>
</div>

<div className="status-text">
  <div className="selected-city">Displaying: {selectedCity}</div>
</div>




      <div className="status-ring-container">
  <div className={`status-ring ${status.toLowerCase()}`}>
    <span className="status-label">{status}</span>
  </div>
</div>

      <div className="buttons">
        <button onClick={fetchNewData}>Fetch New Data</button>
        <button onClick={getLatestRecords}>Show Records</button>
      </div>

      


      {notification && <p className="notification">{notification}</p>}

      {messages.length > 0 && (
  <div className="messages">
    <h3>Fetch Log</h3>
    <ul>
      {messages
        .filter((msg) => selectedCity === "All" || msg.toLowerCase().includes(selectedCity.toLowerCase()))
        .map((msg, i) => (
          <li key={i}>{msg}</li>
        ))}
    </ul>
  </div>
)}


{weatherData.length > 0 && (
  <table>
    <thead>
      <tr>
        <th>City</th>
        <th>Temperature (°C)</th>
        <th>Humidity</th>
        <th>Pressure</th>
        <th>Timestamp</th>
      </tr>
    </thead>
    <tbody>
    {weatherData
  .filter((entry) => selectedCity === "All" || entry.place === selectedCity)
  .map((entry) => (
    <tr key={entry.id}>
      <td>{entry.place}</td>
      <td>{entry.temperature}</td>
      <td>{entry.humidity}</td>
      <td>{entry.pressure}</td>
      <td>{entry.timestamp}</td>
    </tr>
  ))}

    </tbody>
  </table>
)}




      <div className="exit-button-container">
  <button className="return-button" onClick={() => setEntered(false)}>
    ⬅️ Exit
  </button>
</div>


    </div>
  );
}

export default App;
