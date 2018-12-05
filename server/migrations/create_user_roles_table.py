create_user_roles_table = """CREATE TABLE IF NOT EXISTS user_roles(
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            role_id INTEGER NOT NULL REFERENCES roles(id)
        )"""