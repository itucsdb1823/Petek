def terms_table_seeder(cur):
    seasons = ['GÜZ', 'BAHAR', 'YAZ']
    terms = ['11/12', '12/13', '13/14', '14/15', '15/16', '16/17', '17/18', '18/19']
    for term in terms:
        for season in seasons:
            cur.execute("""INSERT INTO terms(season, term_year) VALUES(%s, %s) returning id""", (season, term))
