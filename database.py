import sqlite3

con = sqlite3.connect('database.db')
cur = con.cursor()

cur.execute('''create table if not EXISTS waifus (
            id          INTEGER,
            code        Varchar(110) UNIQUE NOT NULL,
            name        varchar(50),
            anime       varchar(50),
            PRIMARY KEY(id));
            ''')


def insert_row(code, name, anime):
    exist = cur.execute("SELECT * FROM waifus WHERE code=?", (str(code),)).fetchone()
    if exist:
        if bool(exist[3]):  # antes se usaba REPLACE INTO
            cur.execute("""
            UPDATE waifus 
            SET code=?,
                name=?
            WHERE
                id=?""", (str(code), str(name), exist[0]))
        else:
            cur.execute("""
            UPDATE waifus
            SET code = ?,
                name = ?,
                anime = ?
            WHERE
                id = ?""", (str(code), str(name), str(anime), exist[0]))

    else:
        cur.execute("INSERT INTO waifus (code,name,anime) VALUES(?,?,?)", (str(code), str(name), str(anime)))
    con.commit()


def get_name(code):
    name = cur.execute("SELECT name FROM waifus WHERE code=?", (str(code),)).fetchone()
    if name:
        return name[0]
    else:
        return False
