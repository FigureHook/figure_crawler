import re
from typing import Union


def price_parse(text: str, remove_tax: bool = False) -> Union[int, None]:
    pattern = r"\d+"
    price_text = ""

    for n in re.findall(pattern, text):
        price_text += n

    try:
        price = int(price_text)
        if remove_tax:
            price = round(price / 1.1)
    except ValueError:
        return None

    return price


def scale_parse(text: str) -> Union[int, None]:
    pattern = r"\d/(\d+)"
    scale_text = re.search(pattern, text)
    scale = int(scale_text.group(1)) if scale_text else None
    return scale


def size_parse(text: str) -> Union[int, None]:
    pattern = r"(\d+)[mm|cm|ｍｍ|ｃｍ]"
    is_cm = bool(re.search(r"cm", text))
    size_text = re.search(pattern, text)

    if not size_text:
        return None

    size = size_text.group(1)

    if is_cm:
        return int(size) * 10

    return int(size)
