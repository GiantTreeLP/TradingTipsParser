from telethon import TelegramClient
from telethon.errors import ChannelPrivateError

# Import api_id and api_hash from private.py
# Provide that file on your own
import private

client = TelegramClient("session1", private.api_id, private.api_hash)
client.session.report_errors = False
client.start()
print(client.get_me())

dialogs = client.iter_dialogs()
for d in dialogs:
    if "NOBLE" not in d.name:
        continue
    print(d.name + ": ")
    try:
        for m in client.get_messages(d.entity, 12)[::-1]:
            author = client.get_entity(m.from_id)
            print(m.date.strftime("%Y-%m-%d %H:%M:%S"), end="")
            print(" ", end="")
            print(author.username if author.username is not None else author.first_name + " " + author.last_name,
                  end="")
            print(": " + m.message)
    except ChannelPrivateError as e:
        print(e)
