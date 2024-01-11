"""This file defines the account model for the application.
It includes classes for User ID, Password, and Hashed Password.
Each class has its own validation methods to ensure the data integrity.
The Password class, for example, checks if the password meets certain requirements
such as length and character composition.
"""
from enum import Enum
from typing import ClassVar, Self

import bcrypt
import pydantic
import sqlmodel

from models import custom_pydantic


class UserID(custom_pydantic.FrozenBaseModel):
    """Wrapper class for the user ID. This class is used to validate the input values."""

    user_id: str = pydantic.Field(min_length=5, max_length=20)


class Password(custom_pydantic.FrozenBaseModel):
    """Wrapper class for the password. This class is used to validate the input values."""

    password: str

    @pydantic.field_validator("password")
    @classmethod
    def validate_password(cls, password: str) -> str:
        """Validates the password.

        This method checks if the password meets the following requirements:
        - It is at least 8 characters long.
        - It contains at least one letter.
        - It contains at least one number.

        Args:
            password (str): The password to be validated.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password does not meet the requirements.
        """
        if len(password) < 8:
            raise ValueError("パスワードは8文字以上である必要があります")
        if not any(char.isalpha() for char in password):
            raise ValueError("パスワードには英字が必要です")
        if not any(char.isdigit() for char in password):
            raise ValueError("パスワードには数字が必要です")
        return password


class HashedPassword(custom_pydantic.FrozenBaseModel):
    """Wrapper class for the hashed password. This class is used to validate the input values."""

    hashed_password: str

    @classmethod
    def from_password(cls, password_model: Password) -> Self:
        """This class method takes in an instance of Password and returns an instance of the class.

        Args:
            password (Password): An instance of Password.

        Returns:
            Self: An instance of the class.
        """
        return cls(hashed_password=bcrypt.hashpw(password_model.password.encode(), bcrypt.gensalt()).decode())

    def verify(self, password_model: Password) -> bool:
        """Verifies if the provided password matches the hashed password.

        This method takes an instance of Password as an argument and checks if it matches the hashed password.

        Args:
            password_model (Password): The password to be verified.

        Returns:
            bool: Returns True if the provided password matches the hashed password, otherwise returns False.
        """
        return bcrypt.checkpw(password_model.password.encode(), self.hashed_password.encode())


class Age(custom_pydantic.FrozenBaseModel):
    """Wrapper class for the age. This class is used to validate the input values."""

    age: int = pydantic.Field(ge=0, le=100)


class Sex(Enum):
    """Enumeration to define Sex options."""

    MALE = "男性"
    FEMALE = "女性"
    OTHER = "その他"


class Account(sqlmodel.SQLModel, table=True):
    """SQL model for the Account table. This class should not be used directly."""

    __table_args__: ClassVar = {"extend_existing": True}

    user_id: str = sqlmodel.Field(primary_key=True)  # need to guarantee uniqueness
    hashed_password: str
    age: int
    sex: str

    @classmethod
    def from_model(
        cls, user_id_model: UserID, hashed_password_model: HashedPassword, age_model: Age, sex: Sex
    ) -> Self:
        """This class method takes in instances of UserID, Password, Age, and returns an instance of the class.

        SQLModel does not support nested models, so this method is used to convert the nested models to a single model.

        Args:
            user_id_model (UserID): An instance of UserID.
            hashed_password_model (HashedPassword): An instance of Password.
            age_model (Age): An instance of Age.
            sex (Sex): An instance of Sex.

        Returns:
            Self: An instance of the class.
        """
        return cls(
            user_id=user_id_model.user_id,
            hashed_password=hashed_password_model.hashed_password,
            age=age_model.age,
            sex=sex.value,
        )
