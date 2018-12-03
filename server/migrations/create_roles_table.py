create_roles_table = """CREATE TABLE IF NOT EXISTS roles(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL
        )"""