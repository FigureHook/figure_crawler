from typing import Type

from src.Factory.product import ProductBase
from src.Models import Product as ProductModel
from src.constants import ReleaseInfoStatus


def compare_release_infos(p_dataclass: Type[ProductBase], p_model: Type[ProductModel]) -> ReleaseInfoStatus:
    p_dataclass.release_infos.sort()
    d_ri = p_dataclass.release_infos
    m_ri = p_model.release_infos
    parsed_dates_set = set((r.release_date for r in d_ri))
    model_dates_set = set(r.initial_release_date for r in m_ri)

    is_conflicted = len(d_ri) < len(m_ri)
    is_new_release = len(d_ri) > len(m_ri)
    same_length = len(d_ri) == len(m_ri)

    if is_conflicted:
        return ReleaseInfoStatus.CONFLICT

    last_release_from_dataclass = d_ri.last()
    last_release_form_model = p_model.last_release()

    if same_length and last_release_form_model and last_release_from_dataclass:
        if None in (parsed_dates_set - model_dates_set):
            return ReleaseInfoStatus.STALLED
        if last_release_from_dataclass.release_date:
            if last_release_from_dataclass.release_date != last_release_form_model.initial_release_date:
                return ReleaseInfoStatus.DELAY

    if parsed_dates_set != model_dates_set:
        if is_new_release:
            return ReleaseInfoStatus.NEW_RELEASE
        return ReleaseInfoStatus.ALTER

    return ReleaseInfoStatus.SAME
