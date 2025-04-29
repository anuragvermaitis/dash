import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Navigation } from "./components/navigation";
import { Header } from "./components/header";
import { Features } from "./components/features";
import { About } from "./components/about";
import { Gallery } from "./components/gallery";
import JsonData from "./data/data.json";
import SmoothScroll from "smooth-scroll";
import "./App.css";

// Components
import UploadCSV from './components/UploadCSV';
import { SignIn } from "./components/SignIn";
import StreamlitEmbed from "./components/StreamlitEmbed"; // <-- NEW

export const scroll = new SmoothScroll('a[href*="#"]', {
  speed: 1000,
  speedAsDuration: true,
});

const App = () => {
  const [landingPageData, setLandingPageData] = useState({});

  useEffect(() => {
    setLandingPageData(JsonData);
  }, []);

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <>
              <Navigation />
              <Header data={landingPageData.Header} />
              <Features data={landingPageData.Features} />
              <About data={landingPageData.About} />
              <Gallery data={landingPageData.Gallery} />
            </>
          }
        />
        <Route path="/signin" element={<SignIn />} />
        <Route path="/uploadcsv" element={<UploadCSV />} />
        <Route path="/upload-dataset" element={<StreamlitEmbed />} /> {/* NEW */}
      </Routes>
    </Router>
  );
};

export default App;
