import os
import re
import time

from bot import WppBot
from consts import Messages
from utils import format_msg_wpp, strip_special_characters
from api import get_data_country, get_data_state, get_data_city


bot = WppBot(name="CoronaBot")
current_msg = ""
old_msg = ""

while True:
    time.sleep(0.3)
    code, current_msg = None, bot.get_last_msg()
    current_msg = current_msg.strip() if current_msg else None

    patterns = r"/covid", r"/ajuda"
    if current_msg == old_msg or current_msg is None or  not len([ p for p in patterns if re.search(p, current_msg) ]):
        continue

    print(f"msg: {current_msg}")

    if re.search(patterns[0], current_msg):
        code, search_term = format_msg_wpp(current_msg)
        print(f"code: {code}, search_term: {search_term}")

    if re.search(patterns[1], current_msg):
        bot.send_msg( Messages.HELP_TEXT.value )

    elif code == "/covid":
        old_msg = current_msg
        data = get_data_country(search_term)

        if data:
            bot.send_media(
                fileToSend=os.path.join(bot.dir_path, "img.png"),
                description=bot.format_msg_country(data, search_term),
            )
            continue

        bot.send_msg( Messages.NOT_FOUND_COUNTRY.value )

    elif code == "/covidbr":
        old_msg = current_msg
        data = get_data_state(search_term)

        if data:
            message, flag = bot.format_msg_state(data, search_term)
            path = os.path.join( bot.dir_path, 'img.png' if flag else 'default.jpeg' )
            bot.send_media( fileToSend=path, description=message )
            continue

        bot.send_msg( Messages.NOT_FOUND_STATE.value )

    elif code == '/covidcity':
        old_msg = current_msg
        data = get_data_city(search_term)

        if data:
            message = bot.format_msg_city(data, search_term)
            bot.send_msg(message)
            continue

        bot.send_msg( Messages.NOT_FOUND_CITY.value )
