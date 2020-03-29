import io
import re
import json
import requests
import unicodedata

from PIL import Image
from typing import Tuple, Dict

from consts import UrlFlag


class ParseDictAsObj(object):
    def __init__(self, data: Dict):
        for key, value in data.items():
            if isinstance(value, (list, Tuple)):
               setattr(
                   self, key, [ParseDictAsObj(k) if isinstance(k, dict) else k for k in value]
                )
            else:
               setattr(
                   self, key, ParseDictAsObj(value) if isinstance(value, dict) else value
                )


def pasrse_json(data):
    result = json.dumps(data, sort_keys=True, indent=4).encode('utf8')

    return json.loads(result)


def strip_accents(string: str) -> str:
    string = unicodedata.normalize("NFD", string)
    string = string.encode("ascii", "ignore")
    string = string.decode("utf-8")

    return string


def strip_special_characters(string: str) -> str:
    patterns = ("", r"[^a-zA-Z0-9_\s_/_]+"), (" ", r"\s\s+"), ("", r"^\s+"), ("", r"\s$")
    result = string

    for item in patterns:
        repl, pattern = item
        regex = re.compile(pattern)
        result = regex.sub(repl=repl, string=result)

    return result


def format_msg_wpp(msg: str) -> Tuple[str, str]:
    try:
        msg = strip_accents(msg)
        msg = strip_special_characters(msg)

        splited_msg = msg.split(' ')
        code = splited_msg[0]
        search_term = splited_msg[1]

        if len(splited_msg) > 2:
            search_term = ' '.join(splited_msg[1:])

        return code, search_term

    except Exception as exc:
        print(f"erro ao tentar formatar menssagem: {exc}")

    return '', ''


def download_img(url):
    try:
        response = requests.get(url, timeout=2, stream=True)

        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            image.save('img.png')

            return True

    except Exception as exc:
        print(f"get img error: {exc}")

    return False

