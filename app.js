import React, { useState, useEffect } from 'react';
import axios from 'axios';

import './App.css'; // Import CSS for styling

function App() {
  const [inputValue, setInputValue] = useState('');
  const [response, setResponse] = useState('');
  const [messageHistory, setMessageHistory] = useState([]);

  useEffect(() => {
    // Scroll to bottom of chat window when new message is added
    const chatWindow = document.getElementById('chat-window');
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }, [messageHistory]);

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return; // Do not send empty messages

    try {
      const response = await axios.post('/api/query', { text: inputValue });
      const responseData = response.data.response;

      setResponse(responseData);
      setMessageHistory([...messageHistory, { message: inputValue, response: responseData }]);
      setInputValue('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Website Chatbot</h1>
      </header>
      <div className="chat-window" id="chat-window">
        {messageHistory.map((messageObj, index) => (
          <div key={index} className="message">
            <p className="user-message">{messageObj.message}</p>
            <p className="bot-message">{messageObj.response}</p>
          </div>
        ))}
        {response && (
          <div className="message">
            <p className="bot-message">{response}</p>
          </div>
        )}
      </div>
      <div className="input-area">
        <input
          type="text"
          placeholder="Type your message here..."
          value={inputValue}
          onChange={handleInputChange}
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
