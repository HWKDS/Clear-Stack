import React, { useState } from "react";

export default function App() {
  const [copied, setCopied] = useState(false);
  const apiUrl = import.meta.env.VITE_OLLAMA_URL || "http://localhost:11434";
  const model = import.meta.env.VITE_OLLAMA_MODEL || "your-model-name";

  return React.createElement(
    "div",
    { style: { fontFamily: "system-ui, sans-serif", padding: 20 } },
    React.createElement("h1", null, "ClearStack — Web Frontend Demo"),
    React.createElement(
      "p",
      null,
      "This is a minimal frontend to verify environment configuration.",
    ),
    React.createElement(
      "dl",
      null,
      React.createElement("dt", null, "Ollama API URL"),
      React.createElement("dd", null, apiUrl),
      React.createElement("dt", null, "Ollama model"),
      React.createElement("dd", null, model),
    ),
    React.createElement(
      "p",
      null,
      "To test your Ollama server, call your backend or the Ollama API from the server-side. Avoid exposing your local host directly from production frontends.",
    ),
    React.createElement(
      "button",
      {
        onClick: async () => {
          await navigator.clipboard?.writeText(
            `VITE_OLLAMA_URL=${apiUrl}\nVITE_OLLAMA_MODEL=${model}`,
          );
          setCopied(true);
          setTimeout(() => setCopied(false), 1500);
        },
        style: { padding: "8px 12px", marginTop: 12 },
      },
      copied ? "Copied .env values" : "Copy .env values",
    ),
  );
}
