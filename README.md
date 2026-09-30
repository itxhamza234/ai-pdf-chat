# AI PDF Chat Platform (with MCP Tool)

Hello! This is a full-stack web application where users can sign up, upload any PDF document, and chat directly with that PDF instead of reading the entire file. 

I built this project in 5 days during my internship preparation to practice core concepts like user authentication, Retrieval-Augmented Generation (RAG), and Model Context Protocol (MCP). The entire project is fully containerized and runs with a single command using Docker Compose.

---

## 🚀 Key Features

* **Complete Authentication:** Users can sign up, verify their email via a 4-digit OTP (using Gmail SMTP), login securely with JWT tokens, and reset passwords if forgotten. Passwords are fully hashed and secure.
* **PDF Chat (RAG Pipeline):** Users can upload a PDF. The backend extracts text, breaks it into smaller chunks, converts them into embeddings locally, and stores them in PostgreSQL using the `pgvector` extension.
* **Smart Answer Delivery:** When a user asks a question, the app finds the most relevant parts of the PDF and sends them to Google Gemini to get an exact answer. If the answer is not in the PDF, Gemini will clearly say so.
* **Local MCP Dictionary Tool:** To save LLM costs and time, if a user asks for a simple word definition (like "what is authentication?"), the system bypasses Gemini and calls a fast local MCP server to fetch the definition.

---

## 🛠️ Tech Stack & Tools

* **Frontend:** React.js (built with Vite + Dockerized)
* **Backend:** FastAPI (Python + Dockerized)
* **Database:** PostgreSQL with `pgvector` extension
* **Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`) running locally on CPU inside the container
* **LLM API:** Google Gemini API (`gemini-3.8-flash`)
* **Deployment:** Multi-container Docker & Docker Compose

### Folder Structure
```text
ai-pdf-chat/
├── backend/
│   ├── core/            # Database connection, JWT security, email OTP, and embeddings
│   ├── models/           # SQLAlchemy database tables (User, OTP, PDF data)
│   ├── routers/          # API routes for login, signup, pdf, and chat
│   ├── schemas/          # Pydantic models for request/response validation
│   ├── Dockerfile        # Backend image configuration
│   ├── main.py           # Main file to run the FastAPI backend
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/pages/         # React pages (Login, Signup, Dashboard, Chat room)
│   └── Dockerfile        # Frontend image configuration
├── mcp-server/
│   ├── server.py          # Local server for the word definition tool
│   └── Dockerfile        # MCP server image configuration
├── docs/                 # ER diagram and SQL database schema files
└── docker-compose.yml     # Orchestrates Database, MCP, Backend, and Frontend
```

---

## ⚙️ How to Setup and Run with Docker

### Prerequisites
Make sure you have **Docker Desktop** installed on your laptop. You will also need a Gemini API key and a Gmail App Password. Please ensure you have around 8-10 GB of free disk space for the initial build, as the backend container installs PyTorch for local embedding generation.

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ai-pdf-chat
   ```

2. **Setup environment variables:**
   Create a `.env` file inside the `backend` folder (you can copy `backend/.env.example`) and add your credentials:
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
   *(Note: `DATABASE_URL` and `MCP_URL` are automatically handled inside `docker-compose.yml` for internal container communication, but they are included here for completeness).*

3. **Start the Entire Application Stack:**
   Run the following command in your main root directory:
   ```bash
   docker compose up --build
   ```
   *The first build takes a few minutes because it downloads the PyTorch environment and the embedding weights inside the backend container layer. Once cached, subsequent startups will take only a few seconds.*

4. **Access the Services:**
   * **Web App Frontend:** `http://localhost:5173`
   * **FastAPI Swagger Docs:** `http://localhost:8000/docs`

5. **Stop the Application:**
   ```bash
   docker compose down
   ```

---

## 💻 How to Use the App
1. Open `http://localhost:5173` in your browser.
2. Sign up with a valid email -> Check your inbox for the OTP -> Enter the OTP to verify.
3. Log in to access your secure dashboard.
4. Upload any PDF file.
5. Go to the chat screen, select your PDF, and start asking questions!

---

## 📊 My Approach & Engineering Decisions

* **Auth First:** I built and tested the signup, login, and email verification routes first through Swagger UI. Once security was working, I started building the AI features.
* **Data Privacy:** Each uploaded PDF and chat history is mapped to a specific `user_id` in the database. This ensures that one logged-in user can never see or access another user's documents.
* **Handling Hallucinations:** I added a strict system prompt to Gemini so that it only answers from the PDF text chunks provided to it. If the answer is missing from the document, it safely says *"I could not find this information in the selected document."*
* **Why MCP?** For common programming or general words, using an external LLM costs API tokens. A local regex routing checks the question type and instantly answers using the local MCP server, making it faster and free.
* **Containerized Machine Learning:** To fulfill the assignment's operational constraints, the entire infrastructure is bundled within Docker Compose. Local embedding execution (`sentence-transformers`) runs strictly within the backend container, ensuring the app works perfectly on any laptop running Docker without needing local python setup.

*  **Demonstration video**
https://drive.google.com/file/d/1h5Y-vgwvRsqMmfQUgkRFlr19YF6hMkhm/view?usp=sharing
