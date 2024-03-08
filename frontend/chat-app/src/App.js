// src/App.js

import React, { useState } from 'react';
import Login from './Login';
import Chat from './Chat';

function App() {
  const [authToken, setAuthToken] = useState(null);
  

  return (
    <div className="App">
      <header className="App-header">
        <h1>Peer-to-Peer Chat App</h1>
        {authToken ? (
          <Chat authToken={authToken} />
        ) : (
          <Login setAuthToken={setAuthToken} />
        )}
      </header>
    </div>
  );
}

export default App;
