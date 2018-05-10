from telethon import TelegramClient
from telethon.tl.types import UpdateShortMessage, UpdateNewChannelMessage

# Import api_id and api_hash from private.py
# Provide that file on your own
import private


def print_message(message):
    print(message.date.strftime("(%Y-%m-%d %H:%M:%S) "), end="")
    entity = client.get_entity(message.user_id)
    if entity.first_name and entity.last_name:
        print(entity.first_name + " " + entity.last_name, end="")
    else:
        print(entity.username, end="")
    print(": ", end="")
    print(message.message)


def print_channel_message(message):
    print(message.date.strftime("(%Y-%m-%d %H:%M:%S) "), end="")
    entity = client.get_entity(message.from_id)
    if entity.first_name and entity.last_name:
        print(entity.first_name + " " + entity.last_name, end="")
    else:
        print(entity.username, end="")
    print(": ", end="")
    print(message.message)


def handle_messages(update):
    print("Got %s" % update)
    if isinstance(update, UpdateShortMessage) and not update.out:
        print_message(update)
    elif isinstance(update, UpdateNewChannelMessage):
        print_channel_message(update.message)


if __name__ == '__main__':
    client = TelegramClient(session="session1",
                            api_id=private.api_id,
                            api_hash=private.api_hash,
                            use_ipv6=True,
                            update_workers=1,
                            spawn_read_thread=False)
    client.session.report_errors = False
    client.start()
    print(client.get_me())

    client.add_event_handler(handle_messages)
    client.idle()
