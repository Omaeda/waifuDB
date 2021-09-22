import asyncio
import re
from bisect import bisect_left

from telethon import TelegramClient, events
from tqdm import tqdm

import credentials
import database
import main

bot = TelegramClient("bot", credentials.API_ID, credentials.API_HASH)

anime_re = re.compile(r"\((.*)\)")
loop = asyncio.get_event_loop()
MIN_MSG_ID = 1370253
row_list = []


@bot.on(events.NewMessage(pattern="kk", outgoing=True))
async def _(evevnt: events.NewMessage.Event):
    global row_list
    print("recolectando lista de mensajes 1")
    msg_image_list = await bot.get_messages(entity=evevnt.chat, search="Add them to your collection by sending",
                                            min_id=MIN_MSG_ID)
    print("recolectando lista de mensajes 2")
    msg_list1 = await bot.get_messages(entity=evevnt.chat, search="Farewell, ", min_id=MIN_MSG_ID)
    print("recolectando lista de mensajes 3")
    msg_list2 = await bot.get_messages(entity=evevnt.chat, search="has been added to your collection!",
                                       min_id=MIN_MSG_ID)
    print("recolectando lista de mensajes 4")
    msg_list3 = await bot.get_messages(entity=evevnt.chat, search="ran away. Better luck next time!", min_id=MIN_MSG_ID)
    print("recolectando lista de mensajes 5")
    msg_list4 = await bot.get_messages(entity=evevnt.chat, search="to your collection, goodbye", min_id=MIN_MSG_ID)
    msg_name_list = sorted(msg_list1 + msg_list2 + msg_list3 + msg_list4, key=lambda msg: msg.id)
    count = 0
    id_list = [msg.id for msg in msg_image_list]
    id_list.reverse()

    msg_name_anime = []

    for msg_name in tqdm(msg_name_list, desc="Procesando mensajes..."):
        try:
            clo = take_closest(id_list, msg_name.id)
            name, anime = extract_name(msg_name.text)
            msg_image = [msg_image for msg_image in msg_image_list if msg_image.id == clo][0]
            msg_name_anime.append((msg_image, name, anime))
            count += 1
        except:
            continue

    for i in tqdm(msg_name_anime, desc="Descargando y procesando imagenes..."):
        await get_row_list(i)

    for row in tqdm(row_list, desc="Guardando en db..."):
        save_to_db(row)

    print("FINALIZADO!!\nSe insertaron {} nuevos registros".format(count))
    row_list = []


async def get_row_list(msg_name_anime):
    image = await bot.download_media(message=msg_name_anime[0], file=bytes)
    code = main.process_image(image)
    row_list.append((code, msg_name_anime[1], msg_name_anime[2]))


def save_to_db(row_tuple):
    database.insert_row(*row_tuple)


def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return after
    else:
        return before


def extract_name(text: str) -> tuple:
    if "Farewell, " in text:
        return text.split("Farewell")[1][:-1], ""
    elif ("ran away. Better luck next time!" in text) or ("has been added to your collection!" in text):
        n_text = text.split(" (")[0]
        if "," in n_text:
            name = n_text
        else:
            name = f", {n_text}"
        anime = re.search(anime_re, text).groups()[0]
        return name, anime
    elif "to your collection, goodbye" in text:
        name = f', {text.split(" to your collection, goodbye ")[0].split("You’ve added ")[1]}'
        return name, ""


# @bot.on(events.NewMessage(pattern="^test", outgoing=True))
async def test(event: events.NewMessage.Event):
    # print(event.stringify())
    reply = await event.message.get_reply_message()
    img = await reply.download_media(file=bytes)
    code = main.process_image(img)
    print(code)


@bot.on(events.NewMessage(incoming=True, chats=[-100345435], from_users=[452135]))
async def hunt(event: events.NewMessage.Event):
    if not event.media:
        return
    i_text = '**A Certain character appeared!**\nAdd them to your collection by sending `/guess [character name]`'
    if not i_text == event.text:
        return
    img = await event.message.download_media(file=bytes)
    code = main.process_image(img)
    name = database.get_name(code)
    if name:
        await asyncio.sleep(8)  # Tiempo de espera para que que moha no llore
        await bot.send_message(event.chat_id, f"/guess {name.split(', ')[1]}")
    else:
        return


# @bot.on(events.NewMessage(outgoing=True, pattern="fola"))
async def get_text(event):
    reply = await event.get_reply_message()
    await bot.send_message("me", reply.text, parse_mode=None)


if __name__ == "__main__":
    with bot:
        print("bot iniciado correctamente")
        bot.run_until_disconnected()
