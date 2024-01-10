"""This module contains custom Pydantic models for data validation."""
from functools import partial

import pydantic

from models import const


class FrozenBaseModel(pydantic.BaseModel):
    """A Pydantic model with a configuration that forbids extra attributes,
    freezes the model to prevent modification, enforces strict type checking,
    and validates both default values and assignments.
    """

    model_config = pydantic.ConfigDict(
        extra="forbid", frozen=True, strict=True, validate_default=True, validate_return=True, from_attributes=True
    )


class BaseModel(pydantic.BaseModel):
    """A Pydantic model with a configuration that forbids extra attributes,
    enforces strict type checking, and validates both default values and assignments.
    """

    model_config = pydantic.ConfigDict(
        extra="forbid",
        strict=True,
        validate_default=True,
        validate_return=True,
        validate_assignment=True,
        revalidate_instances="always",
        from_attributes=True,
    )


def make_option_validator(valid_options: set[str], value: str) -> str:
    """Validates the input value against a set of valid options.

    This function ensures that all elements in the input string are included in the set of valid options.

    Args:
        valid_options (set[str]): A set containing the valid options.
        value (str): The input value to be validated.

    Returns:
        str: The validated input value.

    Raises:
        ValueError: If the input value contains options that are not in the valid options set.
    """
    if not value:
        return value
    value_options = {option.strip() for option in value.split(", ")}
    if invalid_values := (value_options - valid_options):
        raise ValueError(
            f"無効な値です: {', '.join(invalid_values)}, 有効な値は{', '.join(valid_options)}, 検証したい値は{value}"
        )
    return value


validate_genre = partial(make_option_validator, {genre.value for genre in const.Genre})
validate_hardware = partial(make_option_validator, {hardware.value for hardware in const.Hardware})
validate_game_format = partial(make_option_validator, {game_format.value for game_format in const.GameFormat})
validate_world_view = partial(make_option_validator, {world_view.value for world_view in const.WorldView})
