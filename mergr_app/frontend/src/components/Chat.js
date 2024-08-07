## frontend/src/components/Chat.js

import React, { useState, useEffect } from 'react';
import { w3cwebsocket as W3CWebSocket } from 'websocket';
import axios from 'axios';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const [username, setUsername] = useState('');
  const [receiver, setReceiver] = useState('');
  const [client, setClient] = useState(null);

  useEffect(() => {
    // Fetch initial chat history
    axios.get('/messages/')
      .then(response => {
        setMessages(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the messages!', error);
      });

    // Initialize WebSocket connection
    const client = new W3CWebSocket('ws://localhost:8000/ws/chat/lobby/');
    client.onopen = () => {
      console.log('WebSocket Client Connected');
    };
    client.onmessage = (message) => {
      const dataFromServer = JSON.parse(message.data);
      if (dataFromServer) {
        setMessages((prevMessages) => [...prevMessages, dataFromServer.message]);
      }
    };
    setClient(client);

    return () => {
      if (client) {
        client.close();
      }
    };
  }, []);

  const sendMessage = () => {
    if (client && message && username && receiver) {
      const messageData = {
        message,
        receiver,
      };
      client.send(JSON.stringify(messageData));
      setMessage('');
    }
  };

  return (
    <div className="chat-container">
      <h2>Chat Room</h2>
      <div className="chat-history">
        {messages.map((msg, index) => (
          <div key={index} className="chat-message">
            <strong>{msg.sender.username}</strong>: {msg.content}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          placeholder="Your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="text"
          placeholder="Receiver username"
          value={receiver}
          onChange={(e) => setReceiver(e.target.value)}
        />
        <input
          type="text"
          placeholder="Type a message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
