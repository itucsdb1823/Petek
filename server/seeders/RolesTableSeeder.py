import sys


def roles_table_seeder(cur, fake, num=10):
    cur.execute("SELECT name, id FROM roles WHERE name='admin'")
    role = cur.fetchone()

    if role is None:
        cur.execute("""INSERT INTO roles(name) VALUES (%s) returning id""", ('admin',))
        role_id = cur.fetchone()[0]
    else:
        role_id = role[1]

    cur.execute("SELECT id FROM users WHERE email='admin@admin.com'")
    admin = cur.fetchone()

    if admin is None:
        cur.execute("""INSERT INTO users(name, email, password, slug, created_at) VALUES (%s, %s, %s, %s, %s) returning id""",
                    ('admin', 'admin@admin.com', '$2b$12$CUDacQIUF3C1OF56.9Mu..TWQbD.cnCjpY8TKl7a9kYkagZvae1dO', 'admin123admin123', '2018-11-11 22:15:47.000000'))
        admin_id = cur.fetchone()[0]
    else:
        admin_id = admin[0]

    cur.execute("""INSERT INTO user_roles(user_id, role_id) VALUES(%s, %s)""",
                (admin_id, role_id))
