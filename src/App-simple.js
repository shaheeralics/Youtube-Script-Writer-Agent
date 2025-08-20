import React, { useState } from 'react';

function App() {
  const [topic, setTopic] = useState('');

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#18181b',
      color: 'white',
      padding: '2rem',
      fontFamily: 'Arial, sans-serif'
    }}>
      <div style={{
        maxWidth: '800px',
        margin: '0 auto',
        textAlign: 'center'
      }}>
        <h1 style={{
          fontSize: '3rem',
          marginBottom: '1rem',
          background: 'linear-gradient(45deg, #0ea5e9, #a855f7)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text'
        }}>
          YouTube Script Writer AI
        </h1>
        
        <p style={{
          fontSize: '1.2rem',
          color: '#a1a1aa',
          marginBottom: '2rem'
        }}>
          Generate compelling YouTube scripts powered by advanced AI
        </p>
        
        <div style={{
          backgroundColor: 'rgba(39, 39, 42, 0.8)',
          padding: '2rem',
          borderRadius: '1rem',
          border: '1px solid rgba(14, 165, 233, 0.3)'
        }}>
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter your video topic..."
            style={{
              width: '100%',
              padding: '1rem',
              backgroundColor: '#27272a',
              border: '1px solid #52525b',
              borderRadius: '0.5rem',
              color: 'white',
              fontSize: '1rem',
              marginBottom: '1rem'
            }}
          />
          
          <button
            onClick={() => alert(`Generating script for: ${topic}`)}
            style={{
              width: '100%',
              padding: '1rem',
              backgroundColor: '#0ea5e9',
              color: 'white',
              border: 'none',
              borderRadius: '0.5rem',
              fontSize: '1rem',
              cursor: 'pointer'
            }}
          >
            Generate Script
          </button>
        </div>
        
        <div style={{
          marginTop: '2rem',
          padding: '1rem',
          backgroundColor: 'rgba(34, 197, 94, 0.1)',
          border: '1px solid rgba(34, 197, 94, 0.3)',
          borderRadius: '0.5rem'
        }}>
          <p>✅ React App is working!</p>
          <p>If you see this, the deployment was successful.</p>
        </div>
      </div>
    </div>
  );
}

export default App;
