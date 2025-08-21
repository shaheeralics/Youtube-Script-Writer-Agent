import React from 'react';
import ReactDOM from 'react-dom/client';

// Simple App without external CSS dependencies
function App() {
  console.log('React App component loaded!');
  
  return React.createElement('div', {
    style: {
      minHeight: '100vh',
      backgroundColor: '#18181b',
      color: 'white',
      padding: '2rem',
      fontFamily: 'Arial, sans-serif',
      textAlign: 'center'
    }
  }, [
    React.createElement('h1', {
      key: 'title',
      style: {
        fontSize: '3rem',
        marginBottom: '1rem',
        background: 'linear-gradient(45deg, #0ea5e9, #a855f7)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent'
      }
    }, 'YouTube Script Writer AI'),
    
    React.createElement('p', {
      key: 'subtitle',
      style: {
        fontSize: '1.2rem',
        color: '#a1a1aa',
        marginBottom: '2rem'
      }
    }, 'React App Successfully Loaded! 🎉'),
    
    React.createElement('div', {
      key: 'success',
      style: {
        padding: '1rem',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        border: '1px solid rgba(34, 197, 94, 0.3)',
        borderRadius: '0.5rem',
        margin: '2rem auto',
        maxWidth: '600px'
      }
    }, [
      React.createElement('p', { key: 'msg1' }, '✅ Deployment successful!'),
      React.createElement('p', { key: 'msg2' }, '✅ React is working!'),
      React.createElement('p', { key: 'msg3' }, '✅ No dependencies issues!')
    ])
  ]);
}

console.log('Starting React app...');

try {
  const root = ReactDOM.createRoot(document.getElementById('root'));
  console.log('Root element found, rendering app...');
  
  root.render(React.createElement(App));
  console.log('App rendered successfully!');
} catch (error) {
  console.error('Error rendering React app:', error);
  
  // Fallback: directly update the DOM
  const rootElement = document.getElementById('root');
  if (rootElement) {
    rootElement.innerHTML = `
      <div style="min-height: 100vh; background: #18181b; color: white; padding: 2rem; text-align: center; font-family: Arial;">
        <h1 style="color: #ef4444;">React App Failed to Load</h1>
        <p>Error: ${error.message}</p>
        <p>Check browser console for details</p>
      </div>
    `;
  }
}
