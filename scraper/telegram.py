import os

import base64

from telethon import TelegramClient

from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetFullChannelRequest


class Telegram:

    def __init__(self):
        # config these variables before your start
        api_id = int(os.environ['API_ID'])
        api_hash = os.environ['API_HASH']
        phone_number = os.environ['PHONE_NUMBER']

        client = TelegramClient(phone_number, api_id, api_hash)
        client.session.report_errors = False
        client.connect()

        if not client.is_user_authorized():
            client.send_code_request(phone_number)
            client.sign_in(phone_number, input('Enter the code: '))

        self.client = client

    def getGroupMemberDetails(self, telegramID):
        result = self.client(GetFullChannelRequest(telegramID))
        file_path = self.client.download_media(
            result.full_chat.chat_photo)
        # with open(file_path, "rb") as image_file:
        #     image = base64.b64encode(image_file.read())
        return {"title": result.chats[0].title, "image": file_path, "member_count": result.full_chat.participants_count, "telegram_description": result.full_chat.about}

    def getUsersInGroup(self, telegramID):
        result = self.client(ResolveUsernameRequest(
            telegramID))
        channel = result.chats[0]

        participant_list = []
        participants = self.client.iter_participants(
            channel, 100000, aggressive=True)
        for participant in participants:
            participant_list.append({
                "id": participant.id,
                "first_name": participant.first_name,
                "last_name": participant.last_name,
                "username": participant.username,
                "bot": participant.bot,
            })
        return participant_list


if __name__ == "__main__":
    tg = Telegram()
    print(tg.getGroupMemberDetails('republicprotocol'))
