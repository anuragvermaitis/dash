import React from "react";

export const About = () => {
  return (
    <div id="about">
      <div className="container">
        <div className="row">
          <div className="col-xs-12 col-md-6">
            <img src="img/about.jpg" className="img-responsive" alt="About Us" />
          </div>
          <div className="col-xs-12 col-md-6">
            <div className="about-text">
              <h2>About Us</h2>
              <p>
               We are a team of aspiring software engineers of college, we made this project for businesses to upload their data and visualize the sales and things with the help of Graph and Plots using python knowledge that we've learnt in college.
              </p>
              <h3>Why Choose Us?</h3>
              <div className="list-style">
                <div className="col-lg-6 col-sm-6 col-xs-12">
                  <ul>
                    <li>Better decision-making</li>
                    <li>Early warning feature</li>
                    <li>Discovering Hidden Opportunities</li>
                  </ul>
                </div>
                <div className="col-lg-6 col-sm-6 col-xs-12">
                  <ul>
                    <li>Competetive Advantages</li>
                    <li>Predicts Future Trends</li>
                    <li>Saves Time & Effort</li>

                    
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
