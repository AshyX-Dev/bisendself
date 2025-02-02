hash_token = "" # Api Hash
id_token = "" # Api ID
me = 000 # Your UID
requirements_path = "reqs.bss" # Bad Words Path

from pyrogram import Client
from pyrogram.types import Message
import requests
import os
import json
import time
import random

locks = []
hearts = [
    '❤',
    '🧡',
    '💛',
    '💙',
    '💚',
    '💜',
    '🖤'
]

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

def createFont(string: str):
    string = string.lower()
    return string.translate(string.maketrans("qwertyuiopasdfghjklzxcvbnm-0123456789", "Qᴡᴇʀᴛʏᴜɪᴏᴘᴀꜱᴅꜰɢʜᴊᴋʟᴢxᴄᴠʙɴᴍ-𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗"))

def getFont(string: str):
    resp = requests.get(f"https://api.codebazan.ir/font/?text={string}")
    resp = resp.json()
    fnts = ''

    if resp['ok']:
        for fnt in resp['result'].keys():
            fnts += fnt + ": " + resp['result'][fnt]
            fnts += "\n"

    else: fnts += "Error in Fetch Fonts - خطا حین گرفتن فونت ها"
    return fnts

def getFall():
    resp = requests.get("https://api.codebazan.ir/fal/?type=json")
    resp = resp.json()

    if resp['Ok']:
        return resp['Result1'], resp['Result']

    else: return "Error in Fetch Fonts - خطا حین گرفتن فونت ها"

@cli.on_message()
def onMessage(_, message: Message):
    message.text = str(message.text).lower()
    if message.from_user.id == me:
        if message.text == "/lock":
            if message.reply_to_message:
                if str(message.reply_to_message.text).isdigit():
                    if not int(str(message.reply_to_message.text)) in locks:
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

                else:
                    if not message.reply_to_message.from_user.id in locks:
                        locks.append(
                            message.reply_to_message.from_user.id
                        )
                        cli.edit_message_text(
                            message.chat.id,
                            message.id,
                            createFont("✅ user added to targets\n⌨ uid: ") + str(message.reply_to_message.from_user.id)
                        )
                    
                    else: cli.edit_message_text(
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
                if str(message.reply_to_message.text).isdigit():
                    if int(str(message.reply_to_message.text)) in locks:
                        locks.remove(
                            int(str(message.reply_to_message.text))
                        )
                        cli.edit_message_text(
                            message.chat.id,
                            message.id,
                            createFont("✅ user removed from targets\n⌨ uid: ") + message.reply_to_message.text
                        )
                    else: cli.edit_message_text(
                        message.chat.id,
                        message.id,
                        createFont("user is not in list yet ♦")
                    )

                elif message.reply_to_message.from_user.id in locks:
                    locks.append(
                        message.reply_to_message.from_user.id
                    )
                    cli.edit_message_text(
                        message.chat.id,
                        message.id,
                        createFont("✅ user removed from targets\n⌨ uid: ") + str(message.reply_to_message.from_user.id)
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
            sents = 0
            itm = 10
            with open(requirements_path, 'r') as file:
                words =  file.read()
                words = words.split("\n")
                for _ in range(itm):
                    if sents != 10:
                        try:
                            cli.send_message(
                                message.chat.id,
                                random.choice(words),
                                reply_to_message_id=message.reply_to_message.id
                            )
                            sents += 1
                        except:itm += 1
                file.close()

        elif message.text == "گلب":
            for _ in hearts:
                cli.edit_message_text(
                    message.chat.id,
                    message.id,
                    _
                )
                time.sleep(0.8)

        elif message.text in ( "لیست", "list", "/list" ):
            targets = list(set(locks))
            cli.edit_message_text(
                message.chat.id,
                message.id,
                "♻ "+json.dumps(
                    targets,
                    indent=2
                )
            )

        elif message.text in ("فال", "fall", "/fall"):
            fall = getFall()
            if isinstance(fall, tuple):
                cli.edit_message_text(
                    message.chat.id,
                    message.id,
                    f"🚩 {fall[0]}\n\n🌐📃 {fall[1]}"
                )

    if message.from_user.id in locks:
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