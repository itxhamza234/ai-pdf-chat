-- AI PDF Chat Platform: database schema (PostgreSQL + pgvector)
-- Matches the SQLAlchemy models in backend/models/

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE users (
    id               SERIAL PRIMARY KEY,
    name             VARCHAR NOT NULL,
    email            VARCHAR NOT NULL UNIQUE,
    hashed_password  VARCHAR NOT NULL,
    is_verified      BOOLEAN DEFAULT FALSE,
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE otps (
    id          SERIAL PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(id),
    code        VARCHAR NOT NULL,
    purpose     VARCHAR NOT NULL,          -- 'email_verification' | 'password_reset'
    is_used     BOOLEAN DEFAULT FALSE,
    expires_at  TIMESTAMPTZ NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE pdf_documents (
    id           SERIAL PRIMARY KEY,
    user_id      INTEGER NOT NULL REFERENCES users(id),
    filename     VARCHAR NOT NULL,
    file_path    VARCHAR NOT NULL,
    uploaded_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE pdf_chunks (
    id         SERIAL PRIMARY KEY,
    pdf_id     INTEGER NOT NULL REFERENCES pdf_documents(id),
    user_id    INTEGER NOT NULL REFERENCES users(id),
    content    TEXT NOT NULL,
    embedding  VECTOR(384) NOT NULL        -- all-MiniLM-L6-v2 = 384 dimensions
);

CREATE TABLE chat_messages (
    id          SERIAL PRIMARY KEY,
    pdf_id      INTEGER NOT NULL REFERENCES pdf_documents(id),
    user_id     INTEGER NOT NULL REFERENCES users(id),
    question    TEXT NOT NULL,
    answer      TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);
