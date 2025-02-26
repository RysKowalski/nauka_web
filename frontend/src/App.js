import React, { useEffect, useState } from "react";
import { fetchMessage } from "./services/api";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchMessage().then((data) => setMessage(data.message));
  }, []);

  return (
    <div>
      <h1>React + FastAPI</h1>
      <p>{message}</p>
    </div>
  );
}

export default App;
