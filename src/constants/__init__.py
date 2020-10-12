from enum import Enum

class BrandHost(str, Enum):
    GSC = "goodsmile.info"
    ALTER = "alter-web.jp"


class GSCCategory(str, Enum):
    SCALE = "scale"
    NENDOROID = "nendoroid_series"
    FIGMA = "figma"
    OTHER_FIGURE = "otherfigures"
    GOODS = "goodsother"
