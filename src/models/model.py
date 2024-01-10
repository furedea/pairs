"""This module defines the Account model for managing user accounts.

Each user account in the application is represented by an instance of the Account model.
"""
import re
from typing import Annotated, ClassVar, Self

import bcrypt
import pydantic
import sqlmodel

from models import const, custom_pydantic


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


class Genre(custom_pydantic.FrozenBaseModel):
    """Wrapper class for the genre. This class is used to validate the input values."""

    genre: Annotated[str, pydantic.AfterValidator(custom_pydantic.validate_genre)]


class Price(custom_pydantic.FrozenBaseModel):
    """Wrapper class for the price. This class is used to validate the input values."""

    low_price: int = pydantic.Field(ge=0, le=10000, multiple_of=1000)
    high_price: int = pydantic.Field(ge=0, le=10000, multiple_of=1000)

    @pydantic.model_validator(mode="after")
    def validate_price(self) -> Self:
        """Validates the price.

        This method checks if the low price is less than or equal to the high price.

        Returns:
            Self: An instance of the class.

        Raises:
            ValueError: If the low price is greater than the high price.
        """
        if self.low_price > self.high_price:
            raise ValueError("最低価格は最高価格以下である必要があります")
        return self

    @property
    def price(self) -> str:
        """Returns the price.

        Returns:
            str: The price.
        """
        return f"{self.low_price}円 ~ {self.high_price}円"


class Hardware(custom_pydantic.FrozenBaseModel):
    """Wrapper class for the hardware. This class is used to validate the input values."""

    hardware: Annotated[str, pydantic.AfterValidator(custom_pydantic.validate_hardware)]


class GameFormat(custom_pydantic.FrozenBaseModel):
    """Wrapper class for the game format. This class is used to validate the input values."""

    game_format: Annotated[str, pydantic.AfterValidator(custom_pydantic.validate_game_format)]


class WorldView(custom_pydantic.FrozenBaseModel):
    """Wrapper class for the world view. This class is used to validate the input values."""

    world_view: Annotated[str, pydantic.AfterValidator(custom_pydantic.validate_world_view)]


class Detail(custom_pydantic.FrozenBaseModel):
    """Wrapper class for the detail. This class is used to validate the input values."""

    detail: str = pydantic.Field(max_length=1000)


class RecommendedGame(custom_pydantic.FrozenBaseModel):
    """Wrapper class for the recommended game. This class is used to validate the input values."""

    recommended_game: str = pydantic.Field(max_length=100)

    @classmethod
    def from_text(cls, recommended_text: str) -> Self:
        """This class method takes in a string containing the recommended game and returns an instance of the class.

        Args:
            recommended_text (str): A string generated by GPT model.

        Returns:
            Self: An instance of the class.
        """
        match: re.Match[str] | None = re.search(r"推薦ゲーム: ([^\n]*)", recommended_text)
        if match is None:
            raise ValueError("予期せぬエラーが発生しました: 推薦ゲームが見つかりませんでした")
        return cls(recommended_game=match.group(1))


class Account(sqlmodel.SQLModel, table=True):
    """SQL model for the Account table. This class should not be used directly."""

    __table_args__: ClassVar = {"extend_existing": True}

    user_id: str = sqlmodel.Field(primary_key=True)  # need to guarantee uniqueness
    hashed_password: str
    age: int
    sex: str

    @classmethod
    def from_model(
        cls, user_id_model: UserID, hashed_password_model: HashedPassword, age_model: Age, sex: const.SexLiteral
    ) -> Self:
        """This class method takes in instances of UserID, Password, Age, and returns an instance of the class.

        SQLModel does not support nested models, so this method is used to convert the nested models to a single model.

        Args:
            user_id_model (UserID): An instance of UserID.
            hashed_password_model (HashedPassword): An instance of Password.
            age_model (Age): An instance of Age.
            sex (const.SexLiteral): An instance of SexLiteral.

        Returns:
            Self: An instance of the class.
        """
        return cls(
            user_id=user_id_model.user_id,
            hashed_password=hashed_password_model.hashed_password,
            age=age_model.age,
            sex=sex,
        )


class History(sqlmodel.SQLModel, table=True):
    """SQL model for the History table. This class should not be used directly."""

    __table_args__: ClassVar = {"extend_existing": True}

    id: int | None = sqlmodel.Field(default=None, primary_key=True)
    user_id: str = sqlmodel.Field(index=True)
    genre: str
    price: str
    hardware: str
    game_format: str
    world_view: str
    detail: str
    recommended_game: str

    @classmethod
    def from_model(
        cls,
        user_id_model: UserID,
        genre_model: Genre,
        price_model: Price,
        hardware_model: Hardware,
        game_format_model: GameFormat,
        world_view_model: WorldView,
        detail_model: Detail,
        recommended_game_model: RecommendedGame,
    ) -> Self:
        """This class method takes in instances of UserID, Genre, Price, Hardware, GameFormat, WorldView, Detail,
        RecommendedGame, and returns an instance of the class.

        SQLModel does not support nested models, so this method is used to convert the nested models to a single model.

        Args:
            user_id_model (UserID): An instance of UserID.
            genre_model (Genre): An instance of Genre.
            price_model (Price): An instance of Price.
            hardware_model (Hardware): An instance of Hardware.
            game_format_model (GameFormat): An instance of GameFormat.
            world_view_model (WorldView): An instance of WorldView.
            detail_model (Detail): An instance of Detail.
            recommended_game_model (RecommendedGame): An instance of RecommendedGame.

        Returns:
            Self: An instance of the class.
        """
        return cls(
            user_id=user_id_model.user_id,
            genre=genre_model.genre,
            price=price_model.price,
            hardware=hardware_model.hardware,
            game_format=game_format_model.game_format,
            world_view=world_view_model.world_view,
            detail=detail_model.detail,
            recommended_game=recommended_game_model.recommended_game,
        )
