create_tokens_table = """CREATE TABLE IF NOT EXISTS tokens (
        user_id INTEGER NOT NULL REFERENCES users(id),
        token VARCHAR(255) PRIMARY KEY UNIQUE,
        revoked BOOLEAN DEFAULT FALSE,
        created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
    )"""