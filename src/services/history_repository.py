"""This file handles operations related to the History model."""
from collections.abc import Sequence

import sqlalchemy
import sqlmodel

from models import exception, model


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
        user_id: model.UserID,
        genre: model.Genre,
        price: model.Price,
        hardware: model.Hardware,
        game_format: model.GameFormat,
        world_view: model.WorldView,
        detail: model.Detail,
        recommended_game: model.RecommendedGame,
    ) -> None:
        """Adds a new history record to the database.

        Args:
            user_id (model.UserID): The user id associated with the history record.
            genre (model.Genre): The genre of the game.
            price (model.Price): The price of the game.
            hardware (model.Hardware): The hardware required for the game.
            game_format (model.GameFormat): The format of the game.
            world_view (model.WorldView): The world view of the game.
            detail (model.Detail): The detail of the game.
            recommended_game (model.RecommendedGame): The recommended game.
        """
        with sqlmodel.Session(self.__engine) as session:
            history = model.History.from_model(
                user_id, genre, price, hardware, game_format, world_view, detail, recommended_game
            )
            session.add(history)
            session.commit()

    def search(self, user_id_model: model.UserID) -> Sequence[model.History]:
        """
        Retrieves all history records linked to a specific user.

        Args:
            user_id_model (model.UserID): The user id model to search for.

        Returns:
            Sequence[model.History]: A collection of history records linked to the user.
        """
        with sqlmodel.Session(self.__engine) as session:
            histories: Sequence[model.History] = session.exec(
                sqlmodel.select(model.History).where(model.History.user_id == user_id_model.user_id)
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
            history: model.History | None = session.get(model.History, history_id)
            # TODO(kaito): 例外処理の最適化
            if history is None:
                raise exception.NotFoundError(f"history_id: {history_id}")
            session.delete(history)
            session.commit()

    def delete_all(self, user_id_model: model.UserID) -> None:
        """Removes all history records linked to a specific user from the database.

        Args:
            user_id (model.UserID): The user ID model to search for.
        """
        with sqlmodel.Session(self.__engine) as session:
            session.exec(sqlmodel.delete(model.History).where(model.History.user_id == user_id_model.user_id))
            session.commit()
