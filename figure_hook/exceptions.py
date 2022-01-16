__all__ = (
    # Error
    'FigureHookError', 'PublishError',
    # Warning
    'FigureHookWarning'
)


class FigureHookError(Exception):
    """Bass class for all figure_hook error"""


class PublishError(FigureHookError):
    """Bass class for Publishers errors"""

    def __init__(self, publisher: object, reason: str, caused_by: object, *args: object) -> None:
        msg = f"'{reason}' caused by {caused_by} from {publisher}, "
        super().__init__(msg, *args)


class FigureHookWarning(UserWarning):
    """Bass class for all figure_hook warning"""
