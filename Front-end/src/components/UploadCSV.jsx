import React, { useState } from 'react';
import axios from 'axios';

const UploadCSV = () => {
  const [file, setFile] = useState(null);
  const [cleanedData, setCleanedData] = useState([]);
  const [plot, setPlot] = useState(null);

  // Handle file input change
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      alert('Please upload a CSV file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Send POST request to Flask backend (adjust the URL as needed)
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Extract cleaned data and plot (in base64 format)
      const { cleaned_data, plot_base64 } = response.data;
      setCleanedData(cleaned_data);
      setPlot(plot_base64);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div>
      <h1>Upload CSV File</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>

      {/* Display cleaned data */}
      <div>
        <h2>Cleaned Data</h2>
        {cleanedData.length > 0 && (
          <table border="1">
            <thead>
              <tr>
                {Object.keys(cleanedData[0]).map((key) => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {cleanedData.map((row, index) => (
                <tr key={index}>
                  {Object.values(row).map((value, idx) => (
                    <td key={idx}>{value}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Display plot if available */}
      {plot && (
        <div>
          <h2>Plot</h2>
          <img src={`data:image/png;base64,${plot}`} alt="Data Plot" />
        </div>
      )}
    </div>
  );
};

export default UploadCSV;
