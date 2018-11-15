def courses_table_seeder(cur, fake, num=10):
    for i in range(0, num):
        cur.execute("""INSERT INTO courses(name) VALUES(%s) returning id""",
                    (str(fake.lexify(text="???", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ")),))
