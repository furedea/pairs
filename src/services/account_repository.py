"""This file handles operations related to the Account model."""
import sqlalchemy
import sqlmodel

from models import const, model


class AccountRepository:
    """A repository for managing Account data in the database."""

    __slots__ = ("__engine",)

    def __init__(self, engine: sqlalchemy.Engine) -> None:
        """Initialize the AccountRepository with a database engine.

        Args:
            engine (sqlalchemy.Engine): The database engine to use for the repository.
        """
        self.__engine = engine

    def add(self, user_id: model.UserID, password: model.Password, age: model.Age, sex: const.Sex) -> None:
        """Add a new account to the database.

        Args:
            user_id (model.UserID): The user ID for the new account.
            password (model.Password): The password for the new account.
            age (model.Age): The age of the account holder.
            sex (const.Sex): The sex of the account holder.

        Raises:
            sqlalchemy.exc.IntegrityError: Raised when the user ID already exists in the database.
        """
        hashed_password = model.HashedPassword.from_password(password)
        with sqlmodel.Session(self.__engine) as session:
            # TODO(kaito): 例外処理の最適化
            session.add(model.Account.from_model(user_id, hashed_password, age, sex))
            session.commit()

    def fetch(self, user_id_model: model.UserID) -> model.Account | None:
        """Fetch an account from the database by user ID model.

        Args:
            user_id_model (model.UserID): The user ID model of the account to fetch.

        Returns:
            model.Account | None: The fetched account if it exists, None otherwise.
        """
        return sqlmodel.Session(self.__engine).get(model.Account, user_id_model.user_id)

    def delete(self, user_id_model: model.UserID) -> None:
        """Removes an account from the database using the user ID.

        Args:
            user_id_model (model.UserID): The user ID model of the account to be removed.

        Raises:
            exception.NotFoundError: Raised when the account is not found in the database.
        """
        with sqlmodel.Session(self.__engine) as session:
            session.delete(session.get(model.Account, user_id_model.user_id))
            session.commit()
