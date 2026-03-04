function ChatMessage({ message }) {

  const isUser = message.role === "user";

  return (
    <div className={`message-row ${isUser ? "user" : "assistant"}`}>
      <div className="bubble">
        {message.content}
      </div>
    </div>
  );

}

export default ChatMessage;