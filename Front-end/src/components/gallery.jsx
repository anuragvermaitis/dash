// import { Image } from "./image";
// import React from "react";

// export const Gallery = (props) => {
//   return (
//     <div id="portfolio" className="text-center">
//       <div className="container">
//         <div className="section-title">
//           <h2>Graph and Plots</h2>
//           <p>
//             These are the graphs generated for visual representation of the data provided by the cliend.
//           </p>
//         </div>
//         <div className="row">
//           <div className="portfolio-items">
//             {props.data
//               ? props.data.map((d, i) => (
//                   <div
//                     key={`${d.title}-${i}`}
//                     className="col-sm-6 col-md-4 col-lg-4"
//                   >
//                     <Image
//                       title={d.title}
//                       largeImage={d.largeImage}
//                       smallImage={d.smallImage}
//                     />
//                   </div>
//                 ))
//               : "Loading..."}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };


import React from "react";

export const Gallery = () => {
  return (
    <div id="portfolio" className="text-center">
      <div className="container">
        <div className="section-title">
          <h2>Graph and Plots</h2>
          <p>
            These are the graphs generated for visual representation of the data provided by the client.
          </p>
        </div>
        <div className="row">
          {Array.from({ length: 9 }, (_, i) => (
            <div key={i} className="col-sm-6 col-md-4 col-lg-4">
              <img
                src={`img/new/${i + 1}.jpeg`}
                alt={`Graph ${i + 1}`}
                style={{
                  width: "100%",
                  height: "250px",
                  objectFit: "cover",
                  marginBottom: "20px",
                  borderRadius: "8px",
                }}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

