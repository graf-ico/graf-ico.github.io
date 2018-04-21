
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

    def getAllTelegramGroups(self):
        self.cur.execute(
            """SELECT telegram, title, member_count, telegram_description, category FROM PROJECTS;""")
        rows = self.cur.fetchall()
        desc = self.cur.description[1:]
        return {row[0]: {desc.name: value for (desc, value) in zip(desc, row[1:])} for row in rows}

    # def getAllTelegramGroupNames(self):
    #     self.cur.execute(
    #         """SELECT telegram FROM PROJECTS;""")
    #     return [row[0] for row in self.cur.fetchall()]

    def getTelegramGroup(self, group):
        self.cur.execute(
            """SELECT telegram, title, member_count, telegram_description, category FROM PROJECTS WHERE telegram = %s;""", [group])

        ret = self.cur.fetchone()
        if ret:
            return {desc.name: value for (desc, value) in zip(self.cur.description, ret)}
        return None

    def getOverlap(self, groupA, groupB):
        sGroupA = quote_identifier(groupA)
        sGroupB = quote_identifier(groupB)
        self.cur.execute(
            """SELECT COUNT(*) FROM GROUPS WHERE %s = 't' AND %s = 't';""", [AsIs(sGroupA), AsIs(sGroupB)])
        return self.cur.fetchone()[0]

    def getOverlaps(self, group):
        self.cur.execute(
            """SELECT telegram FROM PROJECTS where telegram <> %s;""", [group])
        others = [row[0] for row in self.cur.fetchall()]

        return {other: self.getOverlap(group, other) for other in others}


if __name__ == "__main__":

    try:
        db = DB()
    except:
        print("unable to connect to the database")
