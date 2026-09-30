AI PDF Chat Platform (with MCP Tool)

Hello! This is a full-stack web application where users can sign up, upload any PDF document, and chat directly with that PDF instead of reading the entire file.

I built this project in 5 days during my internship preparation to practice core concepts like user authentication, Retrieval-Augmented Generation (RAG), and Model Context Protocol (MCP).

🚀 Key Features
Complete Authentication: Users can sign up, verify their email via a 4-digit OTP (using Gmail SMTP), login securely with JWT tokens, and reset passwords if forgotten. Passwords are fully hashed and secure.
PDF Chat (RAG Pipeline): Users can upload a PDF. The backend extracts text, breaks it into smaller chunks, converts them into embeddings locally, and stores them in PostgreSQL using the pgvector extension.
Smart Answer Delivery: When a user asks a question, the app finds the most relevant parts of the PDF and sends them to Google Gemini to get an exact answer. If the answer is not in the PDF, Gemini will clearly say so.
Local MCP Dictionary Tool: To save LLM costs and time, if a user asks for a simple word definition (like "what is authentication?"), the system bypasses Gemini and calls a fast local MCP server to fetch the definition.
🛠️ Tech Stack & Tools
Frontend: React.js (built with Vite)
Backend: FastAPI (Python)
Database: PostgreSQL with pgvector extension
Embeddings: sentence-transformers (all-MiniLM-L6-v2) running locally on CPU
LLM API: Google Gemini API (gemini-3.8-flash)
Libraries Used: PyJWT, bcrypt, pypdf, Pydantic
Deployment: Docker and Docker Compose
Folder Structure
text
ai-pdf-chat/
├── backend/
│   ├── core/             # Database connection, JWT security, email OTP, and embeddings
│   ├── models/           # SQLAlchemy database tables (User, OTP, PDF data)
│   ├── routers/          # API routes for login, signup, pdf, and chat
│   ├── schemas/          # Pydantic models for request/response validation
│   ├── Dockerfile        # Backend image
│   ├── main.py           # Main file to run the FastAPI backend
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/pages/        # React pages (Login, Signup, Dashboard, Chat room)
│   └── Dockerfile        # Frontend image
├── mcp-server/
│   ├── server.py         # Local server for the word definition tool
│   └── Dockerfile        # MCP server image
├── docs/                 # ER diagram and SQL schema
└── docker-compose.yml    # Runs the database, MCP server, backend and frontend
🗄️ Database Schema

Show Image

The full SQL schema is available in docs/database_schema.sql.

⚙️ How to Setup and Run
Prerequisites

Make sure you have Docker Desktop installed on your laptop. You will also need a Gemini API key and a Gmail App Password. Keep around 8 GB of free disk space, because the backend image includes PyTorch.

Clone the repository:
bash
   git clone <your-repo-url>
   cd ai-pdf-chat
Setup environment variables: Copy backend/.env.example to backend/.env and add your own credentials:
env
   DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/pdf_chat_db
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_gmail_app_password
   MAIL_FROM=your_email@gmail.com
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   GEMINI_API_KEY=your_key_here
   SECRET_KEY=your_random_secret_key
   MCP_URL=http://localhost:8001/mcp

(DATABASE_URL and MCP_URL are already overridden inside docker-compose.yml for the containers, so you only need them if you run the backend outside Docker.)

Start everything with Docker Compose:
bash
   docker compose up --build

The first build takes a few minutes because PyTorch and the embedding model have to be downloaded. After that, it starts much faster. This one command runs the database, the MCP server, the backend and the frontend.

Open the app:
App: http://localhost:5173
Swagger UI: http://localhost:8000/docs
Stop the app:
bash
   docker compose down
Running without Docker (optional)

If you want to run the backend and frontend directly on your machine, you need Python 3.11+ and Node.js. Start only the database and the MCP server in Docker:

bash
docker compose up -d db mcp-server

Run the backend:

bash
cd backend
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate      
# Activate virtual environment (Mac/Linux)
source .venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload

Run the frontend (open a new terminal):

bash
cd frontend
npm install
npm run dev
💻 How to Use the App
Open http://localhost:5173 in your browser.
Sign up with a valid email -> Check your inbox for the OTP -> Enter the OTP to verify.
Log in to access your secure dashboard.
Upload any PDF file.
Go to the chat screen, select your PDF, and start asking questions!
You can also view backend API endpoints via Swagger UI at http://127.0.0.1:8000/docs.
📊 My Approach & Engineering Decisions
Auth First: I built and tested the signup, login, and email verification routes first through Swagger UI. Once security was working, I started building the AI features.
Data Privacy: Each uploaded PDF and chat history is mapped to a specific user_id in the database. This ensures that one logged-in user can never see or access another user's documents.
Handling Hallucinations: I added a strict system prompt to Gemini so that it only answers from the PDF text chunks provided to it. If the answer is missing from the document, it safely says "I could not find this information in the selected document."
Why MCP? For common programming or general words, using an external LLM costs API tokens. A local regex routing checks the question type and instantly answers using the local MCP server, making it faster and free.


## 🗄️ Database Schema

![ER Diagram](docs/er_diagram.png)

The full SQL schema is available in [`docs/database_schema.sql`](docs/database_schema.sql).