create_users_table = """CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            name varchar(255) NOT NULL,
            email varchar(255) UNIQUE NOT NULL,
            password varchar(255) NOT NULL,
            confirmation_code varchar(255) NULL,
            confirmed boolean NOT NULL DEFAULT FALSE,
            banned boolean NOT NULL DEFAULT FALSE,
            slug varchar(255) UNIQUE,
            created_at timestamp NOT NULL,
            profile_picture varchar(255)
        )
    """