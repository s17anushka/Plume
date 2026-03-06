# Plume

Plume is an AI-powered conversational web application designed to provide supportive interactions through a chat interface. The system integrates a modern React frontend with a serverless backend and an AI-driven agent architecture.

The backend is implemented using Azure Functions and includes multiple agent modules responsible for classification, emotional profiling, conversation memory, and response generation using the Gemini API.

The application is deployed using Azure Static Web Apps with automated CI/CD through GitHub Actions.

---

## Tech Stack

### Frontend
- React 
- Vite
- CSS

### Authentication
- Microsoft Authentication Library (MSAL)
- Microsoft Identity Platform

### Backend
- Azure Functions (Serverless)
- Python

### AI Integration
- Google Gemini API
- Agent-based conversation orchestration

### Cloud Platform
- Azure Static Web Apps

### Storage
- Browser Local Storage (conversation history)

---

## Features

### Microsoft Authentication
Users sign in using their Microsoft account via MSAL authentication.

### Conversational Chat Interface
Users interact with a chat interface that sends messages to the backend API.

### AI Response Generation
User inputs are processed by the backend and sent to the Gemini API to generate contextual responses.

### Agent-based Processing
The backend includes modular AI components that perform different roles in the conversation pipeline.

These include:
- message classification
- emotional profiling
- conversation memory tracking
- response strategy selection
- orchestration of the response generation pipeline

### Conversation History
Chat conversations are stored locally in the browser using `localStorage`.

### Serverless Backend
The backend API runs as an Azure Function and is exposed through the `/api` route.

---

## Architecture

```
User Interface (React + Vite)
            │
            │  MSAL Authentication
            ▼
Azure Static Web Apps
            │
            │  /api/chat
            ▼
Azure Function (Python)
            │
            ▼
Agent Orchestrator
   │        │         │
   ▼        ▼         ▼
Classifier  Emotion   Memory
            Profile
                │
                ▼
          Strategy Engine
                │
                ▼
            Gemini API
                │
                ▼
       AI Response returned
```

---

## Project Structure

```
Plume
│
├── frontend
│   ├── src
│   │   ├── components
│   │   │   ├── ChatMessage.jsx
│   │   │   └── LoadingIndicator.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── authConfig.js
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── serverless-backend
│   ├── agent
│   │   ├── classifier.py
│   │   ├── crisis_engine.py
│   │   ├── emotional_profile.py
│   │   ├── memory.py
│   │   ├── mood_tracker.py
│   │   ├── orchestrator.py
│   │   ├── prompts.py
│   │   └── strategy_engine.py
│   │
│   ├── function_app.py
│   └── host.json
|   |__requirements.txt
│
└── README.md
```

---

## Running the Frontend Locally

Clone the repository

```
git clone https://github.com/s17anushka/Plume.git
```

Navigate to the frontend

```
cd frontend
```

Install dependencies

```
npm install
```

Run development server

```
npm run dev
```

The app will run at

```
http://localhost:5173
```

---

## Deployment

The project is deployed using **Azure Static Web Apps**.

Deployment pipeline:

1. Code pushed to GitHub
2. GitHub Actions builds the React application
3. Azure Static Web Apps deploys the frontend
4. Azure Functions runs the serverless backend
5. Backend communicates with the Gemini API to generate responses

---

## Current Status

The project includes:

- React chat interface
- Microsoft authentication
- Serverless backend with Azure Functions
- Modular AI agent architecture
- Gemini API integration
- Local conversation storage
- Automated cloud deployment pipeline

---
## System Architecture

```mermaid
flowchart TD

U[User] --> FE[React Frontend]

FE --> SWA[Azure Static Web Apps]

SWA --> API[Azure Function API]

API --> ORCH[Agent Orchestrator]

ORCH --> CLS[Classifier]
ORCH --> EMO[Emotional Profile]
ORCH --> MEM[Conversation Memory]
ORCH --> MOOD[Mood Tracker]
ORCH --> STRAT[Strategy Engine]

STRAT --> GEMINI[Gemini API]

GEMINI --> RESP[AI Generated Response]

RESP --> FE
