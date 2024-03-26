import React from 'react';

function App() {
  return (
    <div classname="App">
      <iframe
        src="http://localhost:8000"  // SERVER_PORT
        title="AutoTA"
        frameBorder="0"
        style={{width: '1200px', height: '580px'}}
      ></iframe>
    </div>
  );
}

export default App;
