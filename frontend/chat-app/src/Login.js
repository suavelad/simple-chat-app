// src/Login.js

import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ setAuthToken }) => {
  const [email, setEmail] = useState('sunday01@example.com');
  const [password, setPassword] = useState('12345678');

  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:8005/api/v1/auth/auth/login/', {
        email,
        password,
      });
      console.info('Login ok:', response.data);

      const { token } = response.data;
      setAuthToken(token);
    } catch (error) {
      console.error('Login failed:', error.message);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <label>
        Email:
        <input
          type="text"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </label>
      <br />
      <label>
        Password:
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </label>
      <br />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default Login;
