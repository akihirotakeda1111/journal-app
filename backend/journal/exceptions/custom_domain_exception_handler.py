"""後方互換のため旧パスから新ハンドラを再エクスポートする。"""

from utils.exceptions.exception_handler import custom_exception_handler

custom_domain_exception_handler = custom_exception_handler

__all__ = ["custom_domain_exception_handler", "custom_exception_handler"]
