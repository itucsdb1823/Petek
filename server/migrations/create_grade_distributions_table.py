create_grade_distributions_table = """CREATE TABLE IF NOT EXISTS grade_distributions (
            id SERIAL PRIMARY KEY,
            lecturer_id INTEGER NOT NULL REFERENCES lecturers(id),
            user_id INTEGER NOT NULL REFERENCES users(id),
            image VARCHAR (255) UNIQUE NOT NULL,
            course_id INTEGER NOT NULL REFERENCES courses(id),
            course_code INTEGER NOT NULL,
            english BOOLEAN DEFAULT FALSE,
            term_id INTEGER REFERENCES terms(id) NOT NULL,
            created_at timestamp NOT NULL
        )
    """