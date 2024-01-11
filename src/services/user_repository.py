"""This file handles operations related to the User model."""
import sqlalchemy
import sqlmodel

from models import account


class UserRepository:
    """A repository for managing user data in the database."""

    __slots__ = ("__engine",)

    def __init__(self, engine: sqlalchemy.Engine) -> None:
        """Initialize the AccountRepository with a database engine.

        Args:
            engine (sqlalchemy.Engine): The database engine to use for the repository.
        """
        self.__engine = engine

    def login(self, user_id_model: account.UserID, password_model: account.Password) -> bool:
        """This method is used to authenticate a user using their user_id and password.

        It first checks if the provided user_id exists in the database. If it does,
        it then uses bcrypt to verify if the provided password matches the stored password for that user_id.

        Args:
            user_id_model (account.UserID): The ID of the user attempting to log in.
            password (account.Password): The password provided by the user attempting to log in.

        Returns:
            bool: Returns True if the user_id exists in the database and the provided password is correct.
                  Returns False otherwise.
        """
        with sqlmodel.Session(self.__engine) as session:
            account_model: account.Account | None = session.get(account.Account, user_id_model.user_id)
        hashed_password = account.HashedPassword(hashed_password=account_model.hashed_password)
        if (account_model is not None) and (hashed_password.verify(password_model)):
            return True
        return False
