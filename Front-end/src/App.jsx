import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Navigation } from "./components/navigation";
import { Header } from "./components/header";
import { Features } from "./components/features";
import { About } from "./components/about";
import { Services } from "./components/services";
import { Gallery } from "./components/gallery";
import { Testimonials } from "./components/testimonials";
import { Team } from "./components/Team";
import JsonData from "./data/data.json";
import SmoothScroll from "smooth-scroll";
import "./App.css";
// Correct import for default export
import UploadCSV from './components/UploadCSV';

// New SignIn component
import { SignIn } from "./components/SignIn";

// import SignupForm from './components/upfo';
// import SigninForm from './components/SigninForm';


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
              <Services data={landingPageData.Services} />
              <Gallery data={landingPageData.Gallery} />
              {/* <Testimonials data={landingPageData.Testimonials} /> */}
              {/* <Team data={landingPageData.Team} /> */}
            </>
          }
        />
        <Route path="/signin" element={<SignIn />} />
        <Route path="/uploadcsv" element={<UploadCSV />} />
      </Routes>
    </Router>
  );
};

export default App;
