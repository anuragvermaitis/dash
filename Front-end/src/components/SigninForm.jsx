import React, { useState } from 'react';
import axios from 'axios';

function SigninForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [message, setMessage] = useState('');

  const handleSignin = async () => {
    try {
      const response = await axios.post('http://localhost:5000/signin', {
        email,
        password
      });

      setToken(response.data.token);
      setMessage('Signin successful! Token received.');
    } catch (error) {
      console.error(error);
      setMessage(error.response?.data?.error || 'Signin failed.');
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Signin</h2>

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

      <button onClick={handleSignin}>Signin</button>

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

export default SigninForm;
