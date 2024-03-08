// src/App.js

import React, { useState } from 'react';
import Login from './Login';
import Chat from './Chat';

function App() {
  const [authData, setAuthData] = useState(null);
  
  

  return (
    <div className="App">
      <header className="App-header">
        <h1>Peer-to-Peer Chat App</h1>
        {authData ? (
          <Chat authData={authData} />
        ) : (
          <Login setAuthData={setAuthData} />
        )}
      </header>
    </div>
  );
}

export default App;
