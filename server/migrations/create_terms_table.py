create_terms_table = """CREATE TABLE IF NOT EXISTS terms(
        id SERIAL PRIMARY KEY,
        season VARCHAR(6),
        term_year VARCHAR(6),
        CONSTRAINT unique_term UNIQUE (season, term_year)
    )"""