hash_token = "" # Api Hash
id_token = "" # Api ID
requirements_path = "reqs.bss" # Bad Words Path

from pyrogram import Client
from pyrogram.types import Message, User
from httpx import Client
import os
import random
import json
import io

locks = []
http = Client()
cli = Client(
    "bsself",
    api_hash=hash_token,
    api_id=id_token
)

if not os.path.exists("bsself.session"):
    cli.start()
    print("[bss] Run Script again")
    exit(1)

if not os.path.exists(requirements_path):
    f = open(requirements_path, "a")
    f.close()

me: User = io.run(cli.get_me())

def createFont(string: str):
    string = string.lower()
    return string.translate(string.maketrans("qwertyuiopasdfghjklzxcvbnm-0123456789", "Qᴡᴇʀᴛʏᴜɪᴏᴘᴀꜱᴅꜰɢʜᴊᴋʟᴢxᴄᴠʙɴᴍ-𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"))

def getFont(string: str):
    if string.isalpha():
        resp = http.get(f"https://api.codebazan.ir/font/?text={string}")
        resp = resp.json()
        fnts = ''

        if resp['ok']:
            for fnt in resp['result'].keys():
                fnts += fnt + ": " + resp['result'][fnt]
                fnts += "\n"

        else: fnts += "Error in Fetch Fonts - خطا حین گرفتن فونت ها"
        return fnts
    
    else:
        resp =  http.get(f"https://api.codebazan.ir/font/?type=fa&text={string}")
        resp = resp.json()
        fnts = ''

        if resp['ok']:
            for fnt in resp['result'].keys():
                fnts += fnt + ": " + resp['result'][fnt]
                fnts += "\n"

        else: fnts += "Error in Fetch Fonts - خطا حین گرفتن فونت ها"
        return fnts

@cli.on_message()
def onMessage(_, message: Message):
    if message.from_user.id == me.id:
        if message.text == "/lock":
            if message.reply_to_message:
                if message.reply_to_message.text.isdigit():
                    if not int(message.reply_to_message.text.isdigit()) in locks:
                        locks.append(
                            int(message.reply_to_message.text)
                        )
                        cli.edit_message_text(
                            message.chat.id,
                            message.id,
                            createFont("✅ user added to targets\n⌨ uid: ") + message.reply_to_message.text
                        )
                    else: cli.edit_message_text(
                        message.chat.id,
                        message.id,
                        createFont("user is already in list ♦")
                    )

                elif not message.reply_to_message.from_user.id in locks:
                    locks.append(
                        message.reply_to_message.from_user.id
                    )
                    cli.edit_message_text(
                        message.chat.id,
                        message.id,
                        createFont("✅ user added to targets\n⌨ uid: ") + str(message.reply_to_message.from_user.id)
                    )
                
                else:  cli.edit_message_text(
                    message.chat.id,
                    message.id,
                    createFont("user is already in list ♦")
                )
            
            else:  cli.edit_message_text(
                message.chat.id,
                message.id,
                createFont("please reply to a message ❗")
            )
        
        elif message.text == "/unlock":
            if message.reply_to_message:
                if message.reply_to_message.text.isdigit():
                    if int(message.reply_to_message.text.isdigit()) in locks:
                        locks.remove(
                            int(message.reply_to_message.text)
                        )
                        cli.edit_message_text(
                            message.chat.id,
                            message.id,
                            createFont("✅ user removed to targets\n⌨ uid: ") + message.reply_to_message.text
                        )
                    else:  cli.edit_message_text(
                        message.chat.id,
                        message.id,
                        createFont("user is already in list ♦")
                    )

                elif message.reply_to_message.from_user.id in locks:
                    locks.append(
                        message.reply_to_message.from_user.id
                    )
                    cli.edit_message_text(
                        message.chat.id,
                        message.id,
                        createFont("✅ user removed to targets\n⌨ uid: ") + str(message.reply_to_message.from_user.id)
                    )
                
                else:  cli.edit_message_text(
                    message.chat.id,
                    message.id,
                    createFont("user is not in list yet ♦")
                )
            
            else:  cli.edit_message_text(
                message.chat.id,
                message.id,
                createFont("please reply to a message ❗")
            )

        elif message.text.startswith("فونت"):
            txt = message.text[4:].strip()
            fnt =  getFont(txt)
            cli.edit_message_text(
                message.chat.id,
                message.id,
                fnt
            )

        elif message.text == "alpha":
            with open(requirements_path, 'r') as file:
                words =  file.read()
                words = words.split("\n")
                for _ in range(10):
                    cli.send_message(
                        message.chat.id,
                        random.choice(words),
                        reply_to_message_id=message.reply_to_message.id
                    )
                
                file.close()

    elif message.from_user.id in locks:
        with open(requirements_path, 'r') as file:
                words =  file.read()
                words = words.split("\n")
                cli.send_message(
                    message.chat.id,
                    random.choice(words),
                    reply_to_message_id=message.reply_to_message.id
                )
                
                file.close()

cli.run()