import React, { useState } from 'react';

export const SignIn = () => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [enteredOtp, setEnteredOtp] = useState('');
  const [isOtpVerified, setIsOtpVerified] = useState(false);

  const handleOtpChange = (value, index) => {
    const updatedOtp = [...otp];
    updatedOtp[index] = value;
    setOtp(updatedOtp);
  };

  const handleSendOtp = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/send-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (data.success) {
        alert(`OTP sent to ${email}`);
        setOtpSent(true);
      } else {
        alert(`Failed to send OTP: ${data.message}`);
      }
    } catch (error) {
      alert('Error sending OTP: ' + error.message);
    }
  };

  const handleOtpSubmit = async () => {
    const joinedOtp = otp.join('');
    try {
      const response = await fetch('http://localhost:5000/api/verify-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, otp: joinedOtp }),
      });

      const data = await response.json();

      if (data.success) {
        alert('OTP Verified!');
        setEnteredOtp(joinedOtp);
        setIsOtpVerified(true);
      } else {
        alert('Incorrect OTP. Try again.');
      }
    } catch (error) {
      alert('Error verifying OTP: ' + error.message);
    }
  };

  const handleSignIn = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/signin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (data.success) {
        alert('Sign-in successful!');
        // Redirect or perform further actions here
      } else {
        alert('Sign-in failed: ' + data.message);
      }
    } catch (error) {
      alert('Error signing in: ' + error.message);
    }
  };

  const handleSignUp = async () => {
    if (password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (data.success) {
        alert('Account created successfully!');
        setIsSignUp(false);
        // Redirect or perform further actions here
      } else {
        alert('Sign-up failed: ' + data.message);
      }
    } catch (error) {
      alert('Error signing up: ' + error.message);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: 'auto', marginTop: '50px' }}>
      <h2>{isSignUp ? 'Sign Up' : 'Sign In'}</h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
      />

      {!isSignUp && (
        <>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
          />
          <button onClick={handleSignIn} style={{ width: '100%', padding: '10px' }}>
            Login
          </button>
          <p style={{ marginTop: '10px' }}>
            Don't have an account?{' '}
            <span onClick={() => setIsSignUp(true)} style={{ color: 'blue', cursor: 'pointer' }}>
              Sign Up
            </span>
          </p>
        </>
      )}

      {isSignUp && (
        <>
          {!otpSent && (
            <button
              onClick={handleSendOtp}
              style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
            >
              Send OTP
            </button>
          )}

          {otpSent && !isOtpVerified && (
            <>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                {otp.map((digit, index) => (
                  <input
                    key={index}
                    type="text"
                    maxLength="1"
                    value={digit}
                    onChange={(e) => handleOtpChange(e.target.value, index)}
                    style={{
                      width: '50px',
                      height: '50px',
                      fontSize: '20px',
                      textAlign: 'center',
                    }}
                  />
                ))}
              </div>
              <button
                onClick={handleOtpSubmit}
                style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
              >
                Verify OTP
              </button>
            </>
          )}

          {isOtpVerified && (
            <>
              <input
                type="password"
                placeholder="Create Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
              />
              <input
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                style={{ width: '100%', marginBottom: '10px', padding: '8px' }}
              />
              <button onClick={handleSignUp} style={{ width: '100%', padding: '10px' }}>
                Register
              </button>
            </>
          )}

          <p style={{ marginTop: '10px' }}>
            Already have an account?{' '}
            <span onClick={() => setIsSignUp(false)} style={{ color: 'blue', cursor: 'pointer' }}>
              Sign In
            </span>
          </p>
        </>
      )}
    </div>
  );
};
