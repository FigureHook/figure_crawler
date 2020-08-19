import re

def scale_parse(text):
    pattern = r"\d/(\d+)"
    scale_text = re.search(pattern, text)
    scale = int(scale_text.group(1)) if scale_text else None
    return scale

def size_parse(text):
    pattern = r"(\d+.)mm"
    size_text = re.search(pattern, text).group(1)
    return int(size_text)