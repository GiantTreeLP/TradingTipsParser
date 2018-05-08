from telethon import TelegramClient

import private

client = TelegramClient("session1", private.api_id, private.api_hash)
client.start()
print(client.get_me())
