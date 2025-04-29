import React from "react";

const StreamlitEmbed = () => {
  return (
    <div style={{ height: "100vh" }}>
      <iframe
        title="Streamlit App"
        src="http://localhost:8501"
        width="100%"
        height="100%"
        frameBorder="0"
      />
    </div>
  );
};

export default StreamlitEmbed;
