"""This file handles operations related to the History model."""
from collections.abc import Sequence

import sqlalchemy
import sqlmodel

from models import account, exception, history


class HistoryRepository:
    """A repository for handling operations related to History model."""

    __slots__ = ("__engine",)

    def __init__(self, engine: sqlalchemy.Engine) -> None:
        """Initialize the AccountRepository with a database engine.

        Args:
            engine (sqlalchemy.Engine): The database engine to use for the repository.
        """
        self.__engine = engine

    def add(
        self,
        user_id: account.UserID,
        genre: history.Genre,
        price: history.Price,
        hardware: history.Hardware,
        game_format: history.GameFormat,
        world_view: history.WorldView,
        detail: history.Detail,
        recommended_game: history.RecommendedGame,
    ) -> None:
        """Adds a new history record to the database.

        Args:
            user_id (account.UserID): The user id associated with the history record.
            genre (history.Genre): The genre of the game.
            price (history.Price): The price of the game.
            hardware (history.Hardware): The hardware required for the game.
            game_format (history.GameFormat): The format of the game.
            world_view (history.WorldView): The world view of the game.
            detail (history.Detail): The detail of the game.
            recommended_game (history.RecommendedGame): The recommended game.
        """
        with sqlmodel.Session(self.__engine) as session:
            history_model = history.History.from_model(
                user_id, genre, price, hardware, game_format, world_view, detail, recommended_game
            )
            session.add(history_model)
            session.commit()

    def search(self, user_id_model: account.UserID) -> Sequence[history.History]:
        """
        Retrieves all history records linked to a specific user.

        Args:
            user_id_model (account.UserID): The user id model to search for.

        Returns:
            Sequence[history.History]: A collection of history records linked to the user.
        """
        with sqlmodel.Session(self.__engine) as session:
            histories: Sequence[history.History] = session.exec(
                sqlmodel.select(history.History).where(history.History.user_id == user_id_model.user_id)
            ).all()
        return histories

    def delete(self, history_id: int) -> None:
        """Removes a specific history record from the database using the history ID.

        Args:
            history_id (int): The ID of the history record to be removed.

        Raises:
            exception.NotFoundError: Raised when the history record is not found in the database.
        """
        with sqlmodel.Session(self.__engine) as session:
            history_model: history.History | None = session.get(history.History, history_id)
            # TODO(kaito): 例外処理の最適化
            if history_model is None:
                raise exception.NotFoundError(f"history_id: {history_id}")
            session.delete(history_model)
            session.commit()

    def delete_all(self, user_id_model: account.UserID) -> None:
        """Removes all history records linked to a specific user from the database.

        Args:
            user_id (model.UserID): The user ID model to search for.
        """
        with sqlmodel.Session(self.__engine) as session:
            session.exec(sqlmodel.delete(history.History).where(history.History.user_id == user_id_model.user_id))
            session.commit()
