// src/Chat.js

import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";
// import axios from 'axios';

const Chat = ({ authToken }) => {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState("");
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    
    if (authToken) {
    const socketInstance = io(`ws://localhost:8005`, {
      path: "/socket.io/",
      query: { token: String(authToken.access), user: 3 },
      transports: ["websocket"],
      upgrade: false
      // autoConnect: false,
    });
    // socketInstance?.connect()

    socketInstance.on("connect", () => {
      console.log("WebSocket connected");
    });

    socketInstance.on("connect_error", (err) => {
      console.log("WebSocket err", err);
    });

    socketInstance.on("disconnect", () => {
      console.log("WebSocket disconnected");
    });

    socketInstance.on("chat.message", (val) => {
      console.log("message ==>", val);
    });


    // setSocket(socketInstance);

    // Clean up the WebSocket connection on component unmount
    return () => {
      
      socketInstance.disconnect();
    };
    }
  }, [authToken]);

  const sendMessage = () => {
    console.log("Attempting to send message");
    if (socket && messageInput.trim() !== "") {
      // setTimeout(() => {
      //     // Your WebSocket connection logic here
      //   }, 1000); // Adjust the delay as needed
      const messageObject = {
        // type: 'chat.message',
        message: messageInput,
      };

      console.log("Sending message:", messageObject);
      try {
        // JSON.parse(JSON.stringify(messageObject));
        // If parsing is successful, it's a valid JSON
        console.log(socket);
        socket.emit("message", messageObject, (ack) => {
          console.log("Message sent acknowledgment:", ack);
        });
      } catch (error) {
        console.error("Invalid JSON format for messageObject:", error);
        // Handle the error or notify the user about the invalid JSON
      } finally {
        console.log("emitted nothing");
        setMessageInput("");
      }
    }
  };

  return (
    <div>
      <div>
        {messages.map((message, index) => (
          <div key={index}>{message.message}</div>
        ))}
      </div>
      <input
        type="text"
        value={messageInput}
        onChange={(e) => setMessageInput(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};
export default Chat;
