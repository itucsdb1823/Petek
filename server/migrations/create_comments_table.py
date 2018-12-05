create_comments_table = """
    DO $$ BEGIN
        CREATE TYPE comment_mode AS ENUM ('lecturers', 'notes');
    EXCEPTION
        WHEN duplicate_object THEN null;
    END $$;
    CREATE TABLE IF NOT EXISTS comments (
        id SERIAL PRIMARY KEY UNIQUE,
        comment TEXT NOT NULL,
        user_id INTEGER NOT NULL REFERENCES users(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        type comment_mode NOT NULL,  
        type_id INTEGER NOT NULL
    );
    """