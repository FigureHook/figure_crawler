from typing import List

from src.constants import ReleaseInfoStatus
from src.Factory.product import ProductBase
from src.Models import Product as ProductModel
from src.Models import ProductReleaseInfo


def compare_release_infos(p_dataclass: ProductBase, p_model: ProductModel) -> ReleaseInfoStatus:
    """Compare the alteration between parsed data(:dataclass:`ProductBase`) and stored data(:model:`Product`)

    1. CONFLICT
        When :prop:`release_infos` in :class:`ProductBase` were less than :prop:`release_infos` in :class:`Product`.
        This might be caused by layout-change from the official.
    2. STALLED
        If `None` is exist in the substraction
        (`set(dates in ProductBase.release_infos)` - `set(initial_release_dates in Product.release_infos)`)
    3. DELAY
        When length of two `release_infos` are same,
        but the last release date of `ProductBase.release_infos` is not equal to `Product.release_infos` last release date.
    4. NEW_RELEASE
        When `ProductBase.release_infos` is more than `Product.release_infos` and the set is different.
    5. ALTER
        If the stauts doesn't meet any condition above, but the set is different.
    6. SAME
        Literally, same.
    """
    p_dataclass.release_infos.sort()
    d_ri = p_dataclass.release_infos
    m_ri: List[ProductReleaseInfo] = p_model.release_infos
    parsed_dates_set = set(r.release_date for r in d_ri)
    model_dates_set = set(r.initial_release_date for r in m_ri)

    is_conflicted = len(d_ri) < len(m_ri)
    if is_conflicted:
        return ReleaseInfoStatus.CONFLICT

    last_release_from_dataclass = d_ri.last()
    last_release_form_model = p_model.last_release()

    same_length = len(d_ri) == len(m_ri)
    if same_length and last_release_form_model and last_release_from_dataclass:
        if None in (parsed_dates_set - model_dates_set):
            return ReleaseInfoStatus.STALLED
        if last_release_from_dataclass.release_date:
            if last_release_from_dataclass.release_date != last_release_form_model.initial_release_date:
                return ReleaseInfoStatus.DELAY

    is_new_release = len(d_ri) > len(m_ri)
    if parsed_dates_set != model_dates_set:
        if is_new_release:
            return ReleaseInfoStatus.NEW_RELEASE
        return ReleaseInfoStatus.ALTER

    return ReleaseInfoStatus.SAME
