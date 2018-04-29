
import os
import psycopg2
from psycopg2.extensions import AsIs
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
                title VARCHAR,
                member_count INT DEFAULT NULL,
                scraped BOOLEAN DEFAULT 'f',
                telegram_description VARCHAR,
                category VARCHAR
            );""")
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS overlapped (
                id VARCHAR UNIQUE NOT NULL
            );""")
        self.conn.commit()

    def getTelegramGroup(self, group):
        self.cur.execute(
            """SELECT * FROM PROJECTS WHERE telegram = %s""", [group])

        ret = self.cur.fetchone()
        if ret:
            return {desc.name: value for (desc, value) in zip(self.cur.description, ret)}
        return None

    def addTelegramGroup(self, group, title, member_count, telegram_description, category):
        sGroup = quote_identifier(group)
        self.cur.execute(
            """INSERT INTO projects (telegram, title, member_count, scraped, telegram_description, category) VALUES (%s, %s, %s, 'f', %s, %s) ON CONFLICT (telegram) DO UPDATE SET member_count = %s;""",
            [group, title, member_count, telegram_description, category, member_count])
        self.cur.execute(
            "ALTER TABLE groups ADD COLUMN IF NOT EXISTS %s BOOLEAN DEFAULT FALSE;",
            [AsIs(sGroup)])
        self.conn.commit()

    def updateTelegramGroup(self, group, row, value):
        sRow = quote_identifier(row)
        self.cur.execute(
            """UPDATE projects SET %s = %s WHERE telegram = %s;""",
            [AsIs(sRow), value, group])
        self.conn.commit()

    def addUserInGroup(self, group, user, commit=True):
        # Sanitized input:
        sGroup = quote_identifier(group)
        self.cur.execute(
            """INSERT INTO users (id, first_name, last_name, username, bot) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING""",
            [user["id"], user["first_name"], user["last_name"], user["username"], user["bot"]])
        self.cur.execute(
            """INSERT INTO groups (id, %s) VALUES (%s, 't') ON CONFLICT (id) DO UPDATE SET %s = 't';""",
            [AsIs(sGroup), user["id"], AsIs(sGroup)])
        if commit:
            self.conn.commit()

    def addUsersInGroup(self, group, users):
        for user in users:
            self.addUserInGroup(group, user, commit=False)
        self.conn.commit()

    def setOverlaps(self, group, overlaps):
        self.cur.execute(
            """INSERT INTO overlapped (id) VALUES (%s) ON CONFLICT (id) DO NOTHING""",
            [group])

        sGroup = quote_identifier(group)

        for overlap in overlaps:
            sOverlap = quote_identifier(overlap)
            self.cur.execute(
                "ALTER TABLE overlapped ADD COLUMN IF NOT EXISTS %s INT DEFAULT 0;",
                [AsIs(sOverlap)])
            self.cur.execute(
                """INSERT INTO overlapped (id, %s) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET %s = %s;""",
                [AsIs(sOverlap), group, overlaps[overlap], AsIs(sOverlap), overlaps[overlap]])
            self.cur.execute(
                """INSERT INTO overlapped (id, %s) VALUES (%s, %s) ON CONFLICT (id) DO UPDATE SET %s = %s;""",
                [sGroup, AsIs(sOverlap), overlaps[overlap], sGroup, overlaps[overlap]])
        self.conn.commit()

    def calculateOverlap(self, groupA, groupB):
        sGroupA = quote_identifier(groupA)
        sGroupB = quote_identifier(groupB)
        self.cur.execute(
            """SELECT COUNT(*) FROM GROUPS WHERE %s = 't' AND %s = 't';""", (AsIs(sGroupA), AsIs(sGroupB)))
        result = self.cur.fetchone()
        return result[0]

    def calculateOverlaps(self, group):
        self.cur.execute(
            """SELECT telegram FROM PROJECTS where telegram <> %s;""", [group])
        others = [row[0] for row in self.cur.fetchall()]

        return {other: self.calculateOverlap(group, other) for other in others}

    def getAllTelegramGroups(self):
        self.cur.execute(
            """SELECT telegram FROM PROJECTS;""")
        rows = self.cur.fetchall()
        return [row[0] for row in rows]


if __name__ == "__main__":

    try:
        db = DB()
    except:
        print("unable to connect to the database")

    for group in db.getAllTelegramGroups():
        print(group)
        db.setOverlaps(group, db.calculateOverlaps(group))
