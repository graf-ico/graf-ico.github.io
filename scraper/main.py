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
            scrapeGroup(db, tg, group)
        except KeyboardInterrupt:
            sys.exit()
        except Exception as err:
            print(err)
            print("Failed to process %s" % (group))


def scrapeGroup(db, tg, group):
    row = db.getTelegramGroup(group)
    if row and row["scraped"]:
        print('Skipping %s...' % (group))
        return
    elif row == None:
        count = tg.getGroupMemberCount(group)
        db.addTelegramGroup(group, count)
    else:
        count = row.member_count

    members = tg.getUsersInGroup(group)
    print("Found %s of %s users in %s" % (0, count, group))
    db.addUsersInGroup(group, members)

    # Mark as being scrapeds
    db.updateTelegramGroup(group, 'scraped', True)


if __name__ == "__main__":
    main()
