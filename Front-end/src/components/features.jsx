import React from "react";

export const Features = () => {
  return (
    <div id="features" className="text-center">
      <div className="container">
        <div className="col-md-10 col-md-offset-1 section-title">
          <h2>Features</h2>
        </div>
        <div className="row">
          <div className="col-xs-6 col-md-3">
            <i className="fa fa-comments-o"></i>
            <h3>Custom Filters</h3>
            <p>Clients can apply filters based on their dataset and see information about specific product and duration</p>
          </div>
          <div className="col-xs-6 col-md-3">
            <i className="fa fa-bullhorn"></i>
            <h3>Efficient PR</h3>
            <p>Good research leads to better and effient PR campaign for better publicity and market expansion</p>
          </div>
          <div className="col-xs-6 col-md-3">
            <i className="fa fa-users"></i>
            <h3>Team Communication</h3>
            <p>Proper data shows that which department is working well and which is not, leading team members to communicate and reach to a better solution</p>
          </div>
          <div className="col-xs-6 col-md-3">
            <i className="fa fa-magic"></i>
            <h3>Prediction Magic</h3>
            <p>Based on previous data, it can even predict upcoming future trends and sales estimation, thus making them future ready</p>
          </div>
        </div>
      </div>
    </div>
  );
};
