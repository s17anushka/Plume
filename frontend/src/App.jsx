import { useState, useEffect, useRef } from "react";
import "./App.css";
import ChatMessage from "./components/ChatMessage";
import LoadingIndicator from "./components/LoadingIndicator";
import { useMsal } from "@azure/msal-react";
import { loginRequest } from "./authConfig";

function App() {

  const { instance, accounts } = useMsal();

  const BACKEND_URL = "api/chat";

  const [conversations, setConversations] = useState([]);
  const [activeChat, setActiveChat] = useState(null);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const chatEndRef = useRef(null);

  const login = () => {
    instance.loginPopup(loginRequest);
  };

  const logout = () => {
    instance.logoutPopup();
  };

  // Load conversations
  useEffect(() => {

    const stored = localStorage.getItem("plume_conversations");

    if (stored) {

      const parsed = JSON.parse(stored);
      setConversations(parsed);
      setActiveChat(parsed[0]);

    } else {

      const firstChat = {
        id: Date.now(),
        title: "New Chat",
        messages: [
          {
            role: "assistant",
            content: "Hi! I'm Plume. How are you feeling today?"
          }
        ]
      };

      setConversations([firstChat]);
      setActiveChat(firstChat);

    }

  }, []);

  // Save conversations
  useEffect(() => {

    if (conversations.length > 0) {
      localStorage.setItem(
        "plume_conversations",
        JSON.stringify(conversations)
      );
    }

  }, [conversations]);

  // Scroll chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeChat]);

  const newChat = () => {

    const chat = {
      id: Date.now(),
      title: "New Chat",
      messages: [
        {
          role: "assistant",
          content: "Hi again! What’s on your mind?"
        }
      ]
    };

    setConversations(prev => [chat, ...prev]);
    setActiveChat(chat);

  };

  const sendMessage = async () => {

    if (!inputMessage.trim()) return;

    const userMessage = inputMessage;

    setInputMessage("");

    const updatedMessages = [
      ...activeChat.messages,
      { role: "user", content: userMessage }
    ];

    updateActiveChat(updatedMessages);

    setIsLoading(true);

    try {

      const res = await fetch(BACKEND_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
      });

      const data = await res.json();

      updateActiveChat([
        ...updatedMessages,
        { role: "assistant", content: data.response }
      ]);

    } catch {

      updateActiveChat([
        ...updatedMessages,
        {
          role: "assistant",
          content: "Connection issue. Please try again."
        }
      ]);

    }

    setIsLoading(false);

  };

  const updateActiveChat = (messages) => {

    const updated = conversations.map(chat =>
      chat.id === activeChat.id
        ? { ...chat, messages }
        : chat
    );

    setConversations(updated);

    setActiveChat({
      ...activeChat,
      messages
    });

  };

  if (accounts.length === 0) {

    return (
      <div className="login-screen">
        <h1>🕊️ Plume</h1>
        <p>Mental Health Support Companion</p>
        <button onClick={login}>
          Login with Microsoft
        </button>
      </div>
    );

  }

  return (

    <div className="layout">

      <div className="sidebar">

        <button className="new-chat" onClick={newChat}>
          + New Chat
        </button>

        {conversations.map(chat => (

          <div
            key={chat.id}
            className="chat-item"
            onClick={() => setActiveChat(chat)}
          >
            {chat.title}
          </div>

        ))}

      </div>

      <div className="main">

        <header className="header">

          <h2>🕊️ Plume</h2>

          <button onClick={logout}>
            Logout
          </button>

        </header>

        <div className="chat-container">

          {activeChat?.messages.map((msg, i) => (
            <ChatMessage key={i} message={msg} />
          ))}

          {isLoading && <LoadingIndicator />}

          <div ref={chatEndRef}></div>

        </div>

        <div className="input-bar">

          <textarea
            placeholder="Share what's on your mind..."
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
          />

          <button onClick={sendMessage}>
            ➤
          </button>

        </div>

      </div>

    </div>

  );

}

export default App;