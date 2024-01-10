"""Module for defining custom exceptions for the application."""
# TODO(kaito): 例外処理の最適化
from typing import Literal


class NotFoundError(Exception):
    """Exception raised when an entity is not found."""

    def __init__(self, entity: Literal["user_id", "history_id"]) -> None:
        super().__init__(f"予期せぬエラーが発生しました: {entity}が存在しません")
