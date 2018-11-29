create_lecturers_table = """CREATE TABLE IF NOT EXISTS lecturers (
            id serial PRIMARY KEY,
            name varchar(255) NOT NULL,
            email varchar(255) UNIQUE NOT NULL,
            slug varchar(255) UNIQUE,
            created_at timestamp NOT NULL,
            user_id INTEGER NOT NULL REFERENCES users(id)
        )
    """