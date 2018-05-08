import private
from getpass import getpass

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, PhoneNumberUnoccupiedError

client = TelegramClient("session1", private.api_id, private.api_hash)
client.connect()
if not client.is_user_authorized():
    number = input("Please enter your phone number: ")
    client.send_code_request(number)
    try:
        code = input("Please enter the authorization code: ")
        myself = client.sign_in(number, code)
    except SessionPasswordNeededError:
        print("Couldn't authenticate using the authorization code, please use your password.")
        password = getpass("Please provide your password instead of the code: ")
        myself = client.sign_in(password=password)
    except PhoneNumberUnoccupiedError:
        print("The number you provided is not associated with a Telegram account, signing you up...")
        myself = client.sign_up(code, input("First name: "), input("Last name: "))
print(client.get_me())
