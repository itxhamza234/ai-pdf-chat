# AI PDF Chat Platform (with MCP Tool)

Hello! This is a full-stack web application where users can sign up, upload any PDF document, and chat directly with that PDF instead of reading the entire file. 

I built this project in 5 days during my internship preparation to practice core concepts like user authentication, Retrieval-Augmented Generation (RAG), and Model Context Protocol (MCP).

---

## 🚀 Key Features

* **Complete Authentication:** Users can sign up, verify their email via a 4-digit OTP (using Gmail SMTP), login securely with JWT tokens, and reset passwords if forgotten. Passwords are fully hashed and secure.
* **PDF Chat (RAG Pipeline):** Users can upload a PDF. The backend extracts text, breaks it into smaller chunks, converts them into embeddings locally, and stores them in PostgreSQL using the `pgvector` extension.
* **Smart Answer Delivery:** When a user asks a question, the app finds the most relevant parts of the PDF and sends them to Google Gemini to get an exact answer. If the answer is not in the PDF, Gemini will clearly say so.
* **Local MCP Dictionary Tool:** To save LLM costs and time, if a user asks for a simple word definition (like "what is authentication?"), the system bypasses Gemini and calls a fast local MCP server to fetch the definition.

---

## 🛠️ Tech Stack & Tools

* **Frontend:** React.js (built with Vite)
* **Backend:** FastAPI (Python)
* **Database:** PostgreSQL with `pgvector` extension
* **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`) running locally on CPU
* **LLM API:** Google Gemini API (`gemini-3.8-flash`)
* **Libraries Used:** PyJWT, bcrypt, pypdf, Pydantic

### Folder Structure
```text
ai-pdf-chat/
├── backend/
│   ├── core/            # Database connection, JWT security, email OTP, and embeddings
│   ├── models/           # SQLAlchemy database tables (User, OTP, PDF data)
│   ├── routers/          # API routes for login, signup, pdf, and chat
│   ├── schemas/          # Pydantic models for request/response validation
│   ├── main.py           # Main file to run the FastAPI backend
│   └── requirements.txt  # Python dependencies
├── frontend/
│   └── src/pages/         # React pages (Login, Signup, Dashboard, Chat room)
├── mcp-server/
│   └── server.py          # Local server for the word definition tool
└── docker-compose.yml     # For running Postgres database
```

---

## ⚙️ How to Setup and Run Locally

### Prerequisites
Make sure you have **Docker Desktop**, **Python 3.11+**, and **Node.js** installed on your laptop. You will also need a Gemini API key and a Gmail App Password.

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ai-pdf-chat
   ```

2. **Setup environment variables:**
   Create a `.env` file inside the `backend` folder (you can copy `.env.example`) and add your credentials:
   ```env
   DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/pdf_chat_db
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_gmail_app_password
   MAIL_FROM=your_email@gmail.com
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   GEMINI_API_KEY=your_key_here
   SECRET_KEY=your_random_secret_key
   MCP_URL=http://localhost:8001/mcp
   ```

3. **Start the Database via Docker:**
   ```bash
   docker compose up -d db mcp-server
   ```

4. **Run the Backend:**
   ```bash
   cd backend
   python -m venv .venv
   
   # Activate virtual environment (Windows)
   .venv\Scripts\activate      
   # Activate virtual environment (Mac/Linux)
   source .venv/bin/activate

   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
   *(Note: I am running the backend code locally instead of inside Docker because downloading heavy ML libraries like PyTorch inside Docker containers takes a lot of time during development).*

5. **Run the Frontend (Open a new terminal):**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

---

## 💻 How to Use the App

1. Open `http://localhost:5173` in your browser.
2. Sign up with a valid email -> Check your inbox for the OTP -> Enter the OTP to verify.
3. Log in to access your secure dashboard.
4. Upload any PDF file.
5. Go to the chat screen, select your PDF, and start asking questions!
6. You can also view backend API endpoints via Swagger UI at `http://127.0.0.1:8000/docs`.

---

## 📊 My Approach & Engineering Decisions

1. **Auth First:** I built and tested the signup, login, and email verification routes first through Swagger UI. Once security was working, I started building the AI features.
2. **Data Privacy:** Each uploaded PDF and chat history is mapped to a specific `user_id` in the database. This ensures that one logged-in user can never see or access another user's documents.
3. **Handling Hallucinations:** I added a strict system prompt to Gemini so that it only answers from the PDF text chunks provided to it. If the answer is missing from the document, it safely says "I could not find this information in the selected document."
4. **Why MCP?** For common programming or general words, using an external LLM costs API tokens. A local regex routing checks the question type and instantly answers using the local MCP server, making it faster and free.
