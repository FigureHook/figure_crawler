import re


def price_parse(text):
    pattern = r"\d+"
    price = ""

    for n in re.findall(pattern, text):
        price += n

    return int(price)


def scale_parse(text):
    pattern = r"\d/(\d+)"
    scale_text = re.search(pattern, text)
    scale = int(scale_text.group(1)) if scale_text else None
    return scale


def size_parse(text):
    pattern = r"(\d+)[mm|cm]"
    is_cm = bool(re.search(r"cm", text))
    size_text = re.search(pattern, text)

    if not size_text:
        return None

    size = size_text.group(1)

    if is_cm:
        return int(size) * 10

    return int(size)
