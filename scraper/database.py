
import os
import psycopg2
import codecs


def quote_identifier(s, errors="strict"):
    # Used for sanitizing columns
    # https://stackoverflow.com/questions/6514274/how-do-you-escape-strings-for-sqlite-table-column-names-in-python

    encodable = s.encode("utf-8", errors).decode("utf-8")

    nul_index = encodable.find("\x00")

    if nul_index >= 0:
        error = UnicodeEncodeError("NUL-terminated utf-8", encodable,
                                   nul_index, nul_index + 1, "NUL not allowed")
        error_handler = codecs.lookup_error(errors)
        replacement, _ = error_handler(error)
        encodable = encodable.replace("\x00", replacement)

    return "\"" + encodable.replace("\"", "\"\"") + "\""


class DB:

    def __init__(self):
        SQL_USERNAME = os.environ['SQL_USERNAME']
        SQL_PASSWORD = os.environ['SQL_PASSWORD']
        self.conn = psycopg2.connect("dbname='iconnect' user='"+SQL_USERNAME +
                                     "' host='localhost' password='"+SQL_PASSWORD+"'")
        self.cur = self.conn.cursor()

    def dropTables(self):
        self.cur.execute(
            """DROP TABLE IF EXISTS groups;""")
        self.cur.execute(
            """DROP TABLE IF EXISTS users;""")
        self.cur.execute(
            """DROP TABLE IF EXISTS projects;""")
        self.conn.commit()

    def createTables(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id int primary key NOT NULL,
                first_name VARCHAR,
                last_name VARCHAR,
                username VARCHAR,
                bot BOOLEAN
            );""")
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS groups (
                id int primary key NOT NULL
            );""")
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS projects (
                id SERIAL UNIQUE,
                telegram VARCHAR UNIQUE NOT NULL,
                member_count INT DEFAULT NULL,
                scraped BOOLEAN DEFAULT 'f'
            );""")
        self.conn.commit()

    def getTelegramGroup(self, group):
        self.cur.execute(
            """SELECT * FROM PROJECTS WHERE telegram = %s""", [group])

        ret = self.cur.fetchone()
        if ret:
            return {desc.name: value for (desc, value) in zip(self.cur.description, ret)}
        return None

    def addTelegramGroup(self, group, member_count):
        sGroup = quote_identifier(group)
        self.cur.execute(
            """INSERT INTO projects (telegram, member_count, scraped) VALUES (%s, %s, 'f') ON CONFLICT (telegram) DO UPDATE SET member_count = %s;""",
            [group, member_count, member_count])
        self.cur.execute(
            "ALTER TABLE groups ADD COLUMN IF NOT EXISTS {} BOOLEAN DEFAULT FALSE;"
            .format(sGroup))
        self.conn.commit()

    def updateTelegramGroup(self, group, row, value):
        sRow = quote_identifier(row)
        self.cur.execute(
            """UPDATE projects SET """ + sRow + """ = %s WHERE telegram = %s;""",
            [value, group])
        self.conn.commit()

    def addUserInGroup(self, group, user, commit=True):
        # Sanitized input:
        sGroup = quote_identifier(group)
        self.cur.execute(
            """INSERT INTO users (id, first_name, last_name, username, bot) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING""",
            [user["id"], user["first_name"], user["last_name"], user["username"], user["bot"]])
        self.cur.execute(
            """INSERT INTO groups (id, {}) VALUES (%s, 't') ON CONFLICT (id) DO UPDATE SET {} = 't';"""
            .format(
                sGroup, sGroup),
            [user["id"]])
        if commit:
            self.conn.commit()

    def addUsersInGroup(self, group, users):
        for user in users:
            self.addUserInGroup(group, user, commit=False)
        self.conn.commit()


if __name__ == "__main__":

    try:
        db = DB()
    except:
        print("unable to connect to the database")

    db.updateTelegramGroup('republicprotocol', 'scraped', True)
