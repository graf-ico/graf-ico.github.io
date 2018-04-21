import telegram
import database
import sys


def main():
    tg = telegram.Telegram()

    try:
        db = database.DB()
    except:
        print("unable to connect to the database")
        return

    groups = []

    for group in groups:
        try:
            scrapeGroup(db, tg, group, 'crypto/project')
        except KeyboardInterrupt:
            sys.exit()
        except Exception as err:
            print(err)
            print("Failed to process %s" % (group))


def scrapeGroup(db, tg, group, category):
    row = db.getTelegramGroup(group)
    if row and row["scraped"]:
        print('Skipping %s...' % (group))
        return
    elif row == None:
        details = tg.getGroupMemberDetails(group)
        db.addTelegramGroup(
            group, details["title"], details["member_count"], category, details["telegram_description"])
    else:
        count = row.member_count

    members = tg.getUsersInGroup(group)
    print("Found %s of %s users in %s" % (0, count, group))
    db.addUsersInGroup(group, members)

    # Mark as being scrapeds
    db.updateTelegramGroup(group, 'scraped', True)


if __name__ == "__main__":
    # main()

    db = database.DB()
    tg = telegram.Telegram()

    db.cur.execute(
        """SELECT telegram FROM PROJECTS;""")
    groups = [row[0] for row in db.cur.fetchall()]

    for group in groups:
        details = tg.getGroupMemberDetails(group)
        print("Title of %s: %s" % (group, details["title"]))
        db.updateTelegramGroup(group, 'title',
                               details["title"])
