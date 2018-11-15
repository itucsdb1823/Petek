create_notes_table = """CREATE TABLE IF NOT EXISTS notes(
            id SERIAL PRIMARY KEY UNIQUE,
            title VARCHAR(255) NOT NULL,
            content TEXT,
            lecturer VARCHAR(255) DEFAULT 'Unknown',
            link VARCHAR(255) NOT NULL,
            slug VARCHAR(255) UNIQUE NOT NULL,
            course_id INTEGER NOT NULL REFERENCES courses(id),
            course_code INTEGER,
            english BOOLEAN DEFAULT FALSE,
            term_id INTEGER REFERENCES terms(id),
            user_id INTEGER NOT NULL REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""