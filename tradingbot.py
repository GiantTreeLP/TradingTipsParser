from telethon import TelegramClient

import private

testing = True

client = TelegramClient(None if testing else "session1", private.api_id, private.api_hash)
client.session.set_dc(2, "149.154.167.40", 80)
client.start()
print(client.get_me())
