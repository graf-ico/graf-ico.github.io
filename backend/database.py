
import os
import psycopg2
from psycopg2.extensions import AsIs
import codecs

cache = {}


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
        return {row[0]: {desc.name: value for (desc, value) in zip(self.cur.description[1:], row[1:])} for row in rows}

    def cachedQuery(self, query, params):
        formatted = query % params
        if formatted in cache:
            return cache[formatted]
        self.cur.execute(query, params)
        result = self.cur.fetchone()
        cache[formatted] = result
        return result

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

    def getOverlaps(self, group):
        sGroup = quote_identifier(group)
        self.cur.execute(
            """SELECT * FROM overlapped where id = %s;""", [group])

        row = self.cur.fetchone()
        if row:
            return {desc.name: col for (col, desc) in zip(row, self.cur.description) if desc.name != "id" and desc.name != sGroup}
        return None


if __name__ == "__main__":

    try:
        db = DB()
    except:
        print("unable to connect to the database")
