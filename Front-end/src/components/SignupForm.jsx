import React, { useState } from 'react';
import axios from 'axios';

function SignupForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState(1); // 1 = signup, 2 = verify OTP
  const [message, setMessage] = useState('');
  const [token, setToken] = useState('');

  const handleSignup = async () => {
    try {
      const response = await axios.post('http://localhost:5000/signup', {
        email,
        password
      });

      setMessage(response.data.message);
      setStep(2); // move to OTP verification
    } catch (error) {
      console.error(error);
      setMessage(error.response?.data?.error || 'Signup failed.');
    }
  };

  const handleVerifyOtp = async () => {
    try {
      const response = await axios.post('http://localhost:5000/verify-otp', {
        email,
        otp
      });

      setToken(response.data.token);
      setMessage('Signup successful! Token received.');
    } catch (error) {
      console.error(error);
      setMessage(error.response?.data?.error || 'OTP verification failed.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Signup</h2>

      {step === 1 && (
        <>
          <input
            type="email"
            placeholder="Enter Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          /><br /><br />
          <input
            type="password"
            placeholder="Enter Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          /><br /><br />
          <button onClick={handleSignup}>Signup</button>
        </>
      )}

      {step === 2 && (
        <>
          <p>An OTP has been sent to your email. Enter it below:</p>
          <input
            type="text"
            placeholder="Enter OTP"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
          /><br /><br />
          <button onClick={handleVerifyOtp}>Verify OTP</button>
        </>
      )}

      {message && <p>{message}</p>}

      {token && (
        <div style={{ marginTop: '20px' }}>
          <h4>JWT Token</h4>
          <textarea value={token} readOnly rows="5" style={{ width: '100%' }}/>
        </div>
      )}
    </div>
  );
}

export default SignupForm;
