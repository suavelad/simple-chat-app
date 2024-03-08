import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";

const Chat = ({ authData }) => {
  const [messages, setMessages] = useState([]);
  const [messageInput, setMessageInput] = useState("");
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    if (authData) {
 

      const socketInstance = io(`ws://localhost:8005`, {
        path: `/ws/chat/${authData.user_info.id }/`, // Use the user ID in the path
        query: { token: String(authData.token.access), user: authData.user_info.id }, // Pass user ID in the query
        transports: ["websocket"],
        upgrade: false,
      });

      socketInstance.on("connect", () => {
        console.log("WebSocket connected");
      });

      socketInstance.on("connect_error", (err) => {
        console.log("WebSocket error", err);
      });

      socketInstance.on("disconnect", () => {
        console.log("WebSocket disconnected");
      });

      socketInstance.on("chat.message", (val) => {
        console.log("message ==>", val);
        setMessages((prevMessages) => [...prevMessages, val]);
      });

      setSocket(socketInstance);

      // Clean up the WebSocket connection on component unmount
      return () => {
        socketInstance.disconnect();
      };
    }
  }, [authData]);

  const sendMessage = () => {
    console.log("Attempting to send message");
    if (socket && messageInput.trim() !== "") {
      const messageObject = {
        message: messageInput,
      };

      console.log("Sending message:", messageObject);
      try {
        socket.emit("message", messageObject, (ack) => {
          console.log("Message sent acknowledgment:", ack);
        });
      } catch (error) {
        console.error("Error sending message:", error);
      } finally {
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
