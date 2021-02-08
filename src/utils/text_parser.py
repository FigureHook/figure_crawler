import re
import unicodedata
from typing import Union, overload


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


@overload
def normalize_product_attr(attr_value: str) -> str: ...
@overload
def normalize_product_attr(attr_value: list[str]) -> list[str]: ...


def normalize_product_attr(attr_value: Union[str, list[str]]) -> Union[str, list[str]]:
    if not attr_value:
        return attr_value

    def normalize(value: str):
        # full-width to half-width
        value = unicodedata.normalize("NFKC", value)
        # remove weird spaces
        value = re.sub(r"\s{1,}", " ", value, 0, re.MULTILINE)
        # replace weird quotation
        value = re.sub(r"’", "'", value, 0)

        return value

    if type(attr_value) is str:
        return normalize(attr_value)

    if type(attr_value) is list:
        if all(type(v) is str for v in attr_value):
            return list(map(normalize, attr_value))

    raise TypeError
