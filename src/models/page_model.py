"""This module defines the Page model for the Streamlit application.

The Page model is used to manage the pages within the application.
Each individual page is represented by an instance of this model.
"""
from enum import Enum
from typing import Protocol, runtime_checkable

import sqlalchemy

import session
from models import const
from pages.private import account_info, delete, history
from pages.public import login, recommend, register


@runtime_checkable
class Page(Protocol):
    """Protocol for a Page in the Streamlit application.

    Attributes:
        __session_manager: The session manager for the page.
        page_id: The unique identifier for the page.
        title: The title of the page.
    """

    __session_manager: session.SessionManager
    title: const.PageTitleLiteral

    def render(self) -> None:
        """Render the page.

        This method should be overridden by each specific page to provide the functionality for rendering the page.
        """


class PageType(Enum):
    """Enumeration to define Page types."""

    LOGIN = login.LoginPage
    REGISTER = register.RegisterPage
    RECOMMEND = recommend.RecommendPage
    ACCOUNT_INFO = account_info.AccountInfoPage
    HISTORY = history.HistoryPage
    DELETE = delete.DeletePage


class PageFactory:
    """A factory class for creating and managing Page objects.

    This class uses the Factory design pattern to create and manage Page objects.
    It provides methods to get a Page object,
    get the title of a Page, and get the IDs of all Pages.
    """

    __slots__ = ("__page_dict",)

    def __init__(self, session_manager: session.SessionManager, engine: sqlalchemy.Engine) -> None:
        """Initializes the PageFactory with a session manager.

        Args:
            session_manager (SessionManager): The session manager for the application.
        """
        self.__page_dict: dict[const.PageIDLiteral, Page] = {
            page_type.name: page_type.value(session_manager, engine) for page_type in PageType
        }

    @property
    def page_ids(self) -> tuple[const.PageIDLiteral, ...]:
        """Get all page IDs.

        Returns:
            tuple[PageIDLiteral, ...]: All page IDs.
        """
        return tuple(self.__page_dict.keys())

    def get_page(self, page_id: const.PageIDLiteral) -> Page:
        """Returns the Page object associated with the given page ID.

        Args:
            page_id (PageIDLiteral): The ID of the page.

        Returns:
            Page: The Page object associated with the given page ID.
        """
        return self.__page_dict[page_id]

    def get_page_title(self, page_id: const.PageIDLiteral) -> const.PageTitleLiteral:
        """Returns the title of the Page associated with the given page ID.

        Args:
            page_id (PageIDLiteral): The ID of the page.

        Returns:
            PageTitleLiteral: The title of the Page associated with the given page ID.
        """
        return self.get_page(page_id).title
