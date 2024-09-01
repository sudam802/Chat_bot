import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleChange = (event) => {
    setInput(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (input.trim()) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: input, sender: "user" },
      ]);

      setInput("");

      try {
        // Make a POST request to the Flask API
        const response = await axios.post("http://127.0.0.1:5000/predict", {
          message: input,
        });

        // Extract the chatbot's response
        const botMessage =
          response.data.intents?.intent || "Sorry, I didn't understand that.";

        setMessages((prevMessages) => [
          ...prevMessages,
          { text: botMessage, sender: "bot" },
        ]);
      } catch (error) {
        console.error("Error:", error);
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: "Sorry, there was an error.", sender: "bot" },
        ]);
      }
    }
  };

  return (
    <div className="chat-container">
      <div
        className="ui inverted menu"
        style={{ display: "flex", alignItems: "center" }}
      >
        <a className="active item">Home</a>
        <a className="item">Messages</a>
        <a className="item">Friends</a>

        {/* Adjusted Bold Text */}
        <div
          className="ui item"
          style={{
            marginLeft: "100px", // Adjust this value to move the text more to the left
            marginRight: "auto", // Keeps the text in place while pushing other items to the right
            fontWeight: "bold",
            fontSize: "28px",
            // Ensures text is centered within its container
          }}
        >
          ChatMax
        </div>

        <a href="">
          <i className="google icon" style={{ color: "#ffffff" }}></i>
        </a>
      </div>

      <form onSubmit={handleSubmit} className="ui form container">
        <div className="field">
          <div className="ui action input">
            <input
              type="text"
              value={input}
              onChange={handleChange}
              placeholder="Type your message here..."
              style={{ width: "400px" }}
            />
            <button type="submit" className="ui button">
              <i class="arrow circle right icon"></i>
            </button>
          </div>
        </div>
      </form>
      {messages.length > 0 && (
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "50vh",
          }}
        >
          <div
            className="ui comments card"
            style={{
              width: "600px", // Set your desired fixed width here
            }}
          >
            {messages.map((message, index) => (
              <div key={index} className={`comment ${message.sender}`}>
                <div>
                  <i class="rocketchat icon" />
                </div>
                <div className="content">
                  <div className="text">{message.text}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
