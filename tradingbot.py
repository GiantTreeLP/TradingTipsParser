import datetime
import hashlib
import re
from typing import Union, Optional

from telethon import TelegramClient
from telethon.network import ConnectionTcpObfuscated
from telethon.tl.types import UpdateShortMessage, UpdateNewChannelMessage, UpdateNewMessage, User, Message, Channel, \
    Chat

# Import api_id and api_hash from private.py
# Provide that file on your own
import private


def get_entity(entity_id: Union[str, int]) -> Union[User, Chat, Channel]:
    try:
        return client.get_entity(entity_id)
    except Exception as e:
        print(e)


def print_private_message(message: Union[UpdateShortMessage, UpdateNewMessage]) -> None:
    entity = None
    if message.user_id:
        entity = get_entity(message.user_id)
    print_message(entity, message.date, message.message)


def print_channel_message(message: Message) -> None:
    if message.from_id:
        entity = get_entity(message.from_id)
    else:
        entity = client.get_entity(message.to_id)
    print_message(entity, message.date, message.message)


def print_message(entity: Optional[Union[User, Chat, Channel]], date: datetime.date, message: str) -> None:
    indent = 0
    date_str = date.strftime("(%Y-%m-%d %H:%M:%S) ")
    indent += len(date_str)
    print(date_str, end="")
    if entity:
        if entity.username:
            indent += len(entity.username)
            print(entity.username, end="")
        elif entity.title:
            indent += len(entity.title)
            print(entity.title, end="")
        else:
            indent += len(entity.first_name)
            print(entity.first_name + " ", end="")
            if entity.last_name:
                indent += len(entity.last_name)
                print(entity.last_name, end="")
    indent += 2
    print(": ", end="")
    print(re.sub('\r?\n', '\r\n' + (' ' * indent), message), flush=True)


def handle_messages(update):
    print("Got %s" % update)
    if isinstance(update, (UpdateShortMessage, UpdateNewMessage)) and not update.out:
        print_private_message(update)
    elif isinstance(update, UpdateNewChannelMessage) and not update.message.out:
        print_channel_message(update.message)
    if update.message.media:
        client.download_media(update.message, "media/")


def handle_cli(line: str) -> None:
    if line == "stop":
        client.disconnect()
        exit(0)


def main():
    phone_num = input("Please enter your phone number: ")
    md5_hash = hashlib.md5()
    md5_hash.update(phone_num.encode("utf-8"))
    print("Using session '%s'" % md5_hash.hexdigest())
    global client
    client = TelegramClient(session=md5_hash.hexdigest(),
                            api_id=private.api_id,
                            api_hash=private.api_hash,
                            update_workers=4,
                            report_errors=False,
                            connection=ConnectionTcpObfuscated)
    client.session.report_errors = False
    client.start(phone=phone_num)
    print(client.get_me())

    trend_channel = get_entity("https://t.me/livetrends")
    print(trend_channel)

    for message in client.iter_messages(trend_channel, limit=10):
        if message.to_id.channel_id == trend_channel.id:
            print_message(trend_channel, message.date, message.message)

    client.add_event_handler(handle_messages)
    while True:
        line = input("> ")
        print(line)
        handle_cli(line)


if __name__ == '__main__':
    client = None
    main()
