import hashlib
from typing import Union

from telethon import TelegramClient, ConnectionMode
from telethon.tl.types import UpdateShortMessage, UpdateNewChannelMessage, UpdateNewMessage, User

# Import api_id and api_hash from private.py
# Provide that file on your own
import private


def get_entity(entity_id: Union[str, int]) -> User:
    try:
        return client.get_entity(entity_id)
    except Exception as e:
        print(e)


def print_message(message):
    print(message.date.strftime("(%Y-%m-%d %H:%M:%S) "), end="")
    entity = get_entity(message.user_id)
    if entity.username:
        print(entity.username, end="")
    else:
        print(entity.first_name, end="")
        if entity.last_name:
            print(" " + entity.last_name, end="")

    print(": ", end="")
    print(message.message, flush=True)


def print_channel_message(message):
    print(message.date.strftime("(%Y-%m-%d %H:%M:%S) "), end="")
    entity = get_entity(message.from_id)
    if entity.username:
        print(entity.username, end="")
    else:
        print(entity.first_name + " ", end="")
        if entity.last_name:
            print(entity.last_name, end="")

    print(": ", end="")
    print(message.message, flush=True)


def handle_messages(update):
    print("Got %s" % update)
    if isinstance(update, (UpdateShortMessage, UpdateNewMessage)) and not update.out:
        print_message(update)
    elif isinstance(update, UpdateNewChannelMessage) and not update.message.out:
        print_channel_message(update.message)


if __name__ == '__main__':
    phone_num = input("Please enter your phone number: ")
    md5_hash = hashlib.md5()
    md5_hash.update(phone_num.encode("utf-8"))
    client = TelegramClient(session=md5_hash.hexdigest(),
                            api_id=private.api_id,
                            api_hash=private.api_hash,
                            use_ipv6=True,
                            update_workers=4,
                            spawn_read_thread=False,
                            connection_mode=ConnectionMode.TCP_OBFUSCATED)
    client.session.report_errors = False
    client.start(phone=phone_num)
    print(client.get_me())

    client.add_event_handler(handle_messages)
    client.idle()
