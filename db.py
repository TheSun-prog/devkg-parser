import sqlite3

con = sqlite3.connect('devkg.db')
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS jobs(
    company TEXT,
    vacancy TEXT,
    salary TEXT,
    type TEXT,
    url TEXT,
    description TEXT
)""")
con.commit()


def insertInfo(values):
    cur.execute('INSERT INTO jobs VALUES(?, ?, ?, ?, ?, ?)', tuple(values))
    con.commit()


def getInfo():
    cur.execute('SELECT * FROM jobs')
    rec = cur.fetchall()
    print(rec)


def getInfoForFilter():
    solution = []
    cur.execute('SELECT * FROM jobs')
    rec = cur.fetchall()

    modifications = "- ( ) / ,"
    removingSymboles = modifications.split()
    removingSymboles.append(' ')

    for el in rec:
        vacancy = el[1].lower().strip()
        description = el[5].lower().strip()
        url = el[4].lower().strip()
        for symbol in removingSymboles:
            vacancy = vacancy.replace(symbol, '')
            description = description.replace(symbol, '')
            url = url.replace(symbol, '')
        solution.append([vacancy, description, url])
    return solution
