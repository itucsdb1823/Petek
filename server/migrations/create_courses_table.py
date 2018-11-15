create_courses_table = """CREATE TABLE IF NOT EXISTS courses(
            id SERIAL PRIMARY KEY,
            name VARCHAR(4) UNIQUE
        )"""