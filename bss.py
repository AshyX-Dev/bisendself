hash_token = "" # Api Hash
id_token = "" # Api ID
me = 000 # Your UID
requirements_path = "reqs.bss" # Bad Words Path

from pyrogram import Client
from pyrogram.types import Message
from manager import BisendDatabaseManager
from pytz import timezone
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
import googlesearch
import requests
import os
import json
import time
import random

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

bdm = BisendDatabaseManager()

if not os.path.exists("bsself.session"):
    cli.start()
    print("[bss] Run Script again")
    exit(1)

if not os.path.exists(requirements_path):
    f = open(requirements_path, "a")
    f.close()

def safe_get(attr, default="null"):
    return attr if attr else default

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

def getTehranTimezone() -> datetime:
    return datetime.now(timezone("Asia/Tehran"))

def getMp3LinksWithTitle(url):
    response = httpx.get(url, headers={
        "User-Agent": FakeUserAgent().random
    })
    if response.status_code != 200:
        print(f"Error: Unable to access {url}")
        return {}
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No Title'
    links = soup.find_all('a')
    mp3_links = [link.get('href') for link in links if link.get('href') and link.get('href').endswith('.mp3')]
    if not mp3_links==[]:
        try:
            return {
        'name': title,
        'url': mp3_links[0]}
        except:...

@cli.on_message()
def onMessage(_, message: Message):
    message.text = str(message.text).lower()
    if message.from_user.id == me:
        if message.text == "/lock":
            if message.reply_to_message:
                if str(message.reply_to_message.text).isdigit():
                    if bdm.addLock(int(str(message.reply_to_message.text)))['status'] != "USER_ALREADY_LOCKED":
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
                    if bdm.addLock(message.reply_to_message.from_user.id)['status'] != "USER_ALREADY_LOCKED":
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
                    if bdm.removeLock(int(str(message.reply_to_message.text)))['status'] != "USER_NOT_LOCKED":
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
                        
                else:
                    if bdm.removeLock(message.reply_to_message.from_user.id)['status'] != "USER_NOT_LOCKED":
                        cli.edit_message_text(
                            message.chat.id,
                            message.id,
                            createFont("✅ user removed from targets\n⌨ uid: ") + str(message.reply_to_message.from_user.id)
                        )
                
                    else: cli.edit_message_text(
                        message.chat.id,
                        message.id,
                        createFont("user is not in list yet ♦")
                    )
            
            else: cli.edit_message_text(
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
            itm = bdm.getAlphaRange()
            with open(requirements_path, 'r') as file:
                words =  file.read()
                words = words.split("\n")
                for _ in range(itm):
                    if sents != itm:
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
            cli.edit_message_text(
                message.chat.id,
                message.id,
                "♻ "+json.dumps(
                    bdm.getLocks(),
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

        elif message.text.startswith("تنظیم مقدار"):
            length = str(message.text)[11:].strip()

            if length.isdigit():
                bdm.setAlphaRange(length)
                cli.edit_message_text(
                    message.chat.id,
                    message.id,
                    createFont(f"seted {length} range for Alpha mode 🍾")
                )
            
            else:
                cli.edit_message_text(
                    message.chat.id,
                    message.id,
                    createFont(f"no digits detected ❌")
                )

        elif message.text in ( "پنل کاربر", "پنل یوزر", "یوزر", "کلاینت", "info", "اطلاعات" ):
            try:
                if not message.reply_to_message.from_user.photo:
                    cli.edit_message_text(
                        message.chat.id,
                        message.id,
                        createFont("🎟 name: ") + safe_get(message.reply_to_message.from_user.first_name) + " - " + safe_get(message.reply_to_message.from_user.last_name) + "\n" +
                        createFont("🎫 uid: ") + str(message.reply_to_message.from_user.id) + "\n" +
                        createFont("👥 language code: ") + safe_get(message.reply_to_message.from_user.language_code) + "\n" +
                        createFont("🕹 phone number: ") + safe_get(message.reply_to_message.from_user.phone_number) + "\n" +
                        createFont("📪 username: ") + safe_get(message.reply_to_message.from_user.username) + "\n" +
                        createFont("🛰 online date: ") + safe_get(message.reply_to_message.from_user.last_online_date) + "\n" +
                        createFont("🧣 next offline date: ") + safe_get(message.reply_to_message.from_user.next_offline_date) + "\n" +
                        "----------" + "\n" +
                        createFont("👾 is bot: ") + str(message.reply_to_message.from_user.is_bot) + "\n" +
                        createFont("🍃 is premium: ") + str(message.reply_to_message.from_user.is_premium) + "\n" +
                        createFont("🤺 is contact: ") + str(message.reply_to_message.from_user.is_contact) + "\n" +
                        createFont("👀 is fake: ") + str(message.reply_to_message.from_user.is_fake) + "\n" +
                        createFont("📠 is deleted: ") + str(message.reply_to_message.from_user.is_deleted) + "\n" +
                        createFont("🔰 is self: ") + str(message.reply_to_message.from_user.is_self) + "\n" +
                        createFont("🐱‍👤 is scam: ") + str(message.reply_to_message.from_user.is_scam) + "\n" +
                        createFont("🚦 is support: ") + str(message.reply_to_message.from_user.is_support) + "\n" +
                        createFont("🍡 is verified: ") + str(message.reply_to_message.from_user.is_verified) + "\n" +
                        createFont("🎃 is mutual contact: ") + str(message.reply_to_message.from_user.is_mutual_contact) + "\n\n" +
                        createFont(f"📁📥 captured from {message.chat.id}") + f" | {message.chat.id}"
                    )

                else:
                    fname = f"photo_{random.randint(100, 9999)}.jpg"
                    cli.download_media(
                        message.reply_to_message.from_user.photo.big_file_id,
                        file_name=fname
                    )
                    cli.delete_messages(message.chat.id, [message.id])
                    cli.send_photo(message.chat.id, "downloads/"+fname,
                        createFont("🎟 name: ") + safe_get(message.reply_to_message.from_user.first_name) + " - " + safe_get(message.reply_to_message.from_user.last_name) + "\n" +
                        createFont("🎫 uid: ") + str(message.reply_to_message.from_user.id) + "\n" +
                        createFont("👥 language code: ") + safe_get(message.reply_to_message.from_user.language_code) + "\n" +
                        createFont("🕹 phone number: ") + safe_get(message.reply_to_message.from_user.phone_number) + "\n" +
                        createFont("📪 username: ") + safe_get(message.reply_to_message.from_user.username) + "\n" +
                        createFont("🛰 online date: ") + safe_get(message.reply_to_message.from_user.last_online_date) + "\n" +
                        createFont("🧣 next offline date: ") + safe_get(message.reply_to_message.from_user.next_offline_date) + "\n" +
                        "----------" + "\n" +
                        createFont("👾 is bot: ") + str(message.reply_to_message.from_user.is_bot) + "\n" +
                        createFont("🍃 is premium: ") + str(message.reply_to_message.from_user.is_premium) + "\n" +
                        createFont("🤺 is contact: ") + str(message.reply_to_message.from_user.is_contact) + "\n" +
                        createFont("👀 is fake: ") + str(message.reply_to_message.from_user.is_fake) + "\n" +
                        createFont("📠 is deleted: ") + str(message.reply_to_message.from_user.is_deleted) + "\n" +
                        createFont("🔰 is self: ") + str(message.reply_to_message.from_user.is_self) + "\n" +
                        createFont("🐱‍👤 is scam: ") + str(message.reply_to_message.from_user.is_scam) + "\n" +
                        createFont("🚦 is support: ") + str(message.reply_to_message.from_user.is_support) + "\n" +
                        createFont("🍡 is verified: ") + str(message.reply_to_message.from_user.is_verified) + "\n" +
                        createFont("🎃 is mutual contact: ") + str(message.reply_to_message.from_user.is_mutual_contact) + "\n\n" +
                        createFont(f"📁📥 captured from {message.chat.id}") + f" | {message.chat.id}"
                    )
                    os.remove("downloads/"+fname)
            
            except Exception as ErrorPro:
                cli.edit_message_text(
                    message.chat.id,
                    message.id,
                    createFont(f"Error: {ErrorPro}")
                )

        elif message.text.startswith("موزیک"):
            music = str(message.text[5:]).strip()
            spl = music.split()
            if spl > 2:
                if spl[0].isdigit():
                    results = [getMp3LinksWithTitle(m) for m in googlesearch.search(music[2:], num_results=int(spl[0]))]
                    for res in results:
                        if isinstance(res, dict):
                            message.delete()
                            message.reply_audio(
                                res['url'],
                                caption="🔉 "+res['name']
                            )
                            continue
                    
                    message.edit_text(
                        createFont("cannot found the music - موزیک پیدا نشد")
                    )

                else:
                    results = [getMp3LinksWithTitle(m) for m in googlesearch.search(music, num_results=5)]
                    for res in results:
                        if isinstance(res, dict):
                            message.delete()
                            message.reply_audio(
                                res['url'],
                                caption="🔉 "+res['name']
                            )
                            continue
                    
                    message.edit_text(
                        createFont("cannot found the music - موزیک پیدا نشد")
                    )

            else:
                results = [getMp3LinksWithTitle(m) for m in googlesearch.search(music, num_results=5)]
                for res in results:
                    if isinstance(res, dict):
                        message.delete()
                        message.reply_audio(
                            res['url'],
                            caption="🔉 "+res['name']
                        )
                        continue
                
                message.edit_text(
                    createFont("cannot found the music - موزیک پیدا نشد")
                )

    if message.from_user.id in bdm.getLocks():
        with open(requirements_path, 'r') as file:
                words =  file.read()
                words = words.split("\n")
                cli.send_message(
                    message.chat.id,
                    random.choice(words),
                    reply_to_message_id=message.id
                )
                
                file.close()

cli.run()