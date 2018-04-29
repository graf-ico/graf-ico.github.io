import telegram
import database
import sys
import os
from PIL import Image, ImageOps, ImageDraw


def main(groups):
    tg = telegram.Telegram()

    try:
        db = database.DB()
    except:
        print("unable to connect to the database")
        return

    for group in groups:
        try:
            scrapeGroup(db, tg, group, 'crypto/project', update=False)
        except KeyboardInterrupt:
            sys.exit()
        except Exception as err:
            print(err)
            print("Failed to process %s" % (group))


def formatImage(group, currentPathname):
    backupPathname = "./original/" + group + ".jpg"
    finalPathname = "../frontend/public/logos/" + group + ".png"

    # os.rename(image, pathname)

    # Mask
    size = (640, 640)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)

    # Read image
    im = Image.open(currentPathname)

    # Save original
    im.save(backupPathname)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    output.save(finalPathname, optimize=True)

    print("Saved image to " + finalPathname)


def scrapeGroup(db, tg, group, category, update=True):
    row = db.getTelegramGroup(group)
    if row and row["scraped"] and (not update):
        print('Skipping %s...' % (group))
        return

    details = tg.getGroupMemberDetails(group)
    db.addTelegramGroup(
        group, details["title"], details["member_count"], details["telegram_description"], category)
    if details["image"]:
        formatImage(group, details["image"])
    count = details["member_count"]

    # Clear current list of users, but don't commit until after adding them back
    db.resetUsersInGroup(group, commit=False)

    members = tg.getUsersInGroup(group)
    print("Found %s of %s users in %s" % (len(members), count, group))
    db.addUsersInGroup(group, members)

    # Set overlaps
    db.setOverlaps(group, db.calculateOverlaps(group))

    # Mark as being scrapeds
    db.updateTelegramGroup(group, 'scraped', True)


if __name__ == "__main__":

    groups = []
    main(groups)
