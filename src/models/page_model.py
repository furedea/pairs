"""This module defines the Page model for the Streamlit application.

The Page model is used to manage the pages within the application.
Each individual page is represented by an instance of this model.
"""
from enum import Enum
from typing import ClassVar, Protocol

import sqlalchemy

import session
from models import const
from pages.private import account_info, delete, history
from pages.public import login, recommend, register


class Page(Protocol):
    """This is a protocol for a Page in the Streamlit application.

    Attributes:
        PAGE_ID: A unique identifier for the page.
        PAGE_TITLE: The title of the page.
        __session_manager: Manages the session for the page.
    """

    PAGE_ID: ClassVar[const.PageID]
    PAGE_TITLE: ClassVar[const.PageTitle]

    __session_manager: session.SessionManager

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

    def create_page(self, session_manager: session.SessionManager, engine: sqlalchemy.Engine) -> Page:
        """Create a Page object for the PageType.

        Returns:
            Page: The Page object for the PageType.
        """
        return self.value(session_manager, engine)


class PageFactory:
    """A factory class for creating and managing Page objects.

    This class uses the Factory design pattern to create and manage Page objects.
    It provides methods to get a Page object by its ID, get the title of a Page,
    and get the IDs of all Pages.
    """

    __slots__ = ("__page_dict",)

    def __init__(self, session_manager: session.SessionManager, engine: sqlalchemy.Engine) -> None:
        """Initializes the PageFactory with a session manager.

        Args:
            session_manager (SessionManager): The session manager for the application.
        """
        self.__page_dict: dict[const.PageID, Page] = {
            page_type.value.PAGE_ID: page_type.create_page(session_manager, engine) for page_type in PageType
        }

    def get_page(self, page_id: const.PageID) -> Page:
        """Get a Page object by its ID.

        Args:
            page_id (PageID): The ID of the Page to get.

        Returns:
            Page: The Page object with the given ID.
        """
        return self.__page_dict[page_id]

    def get_page_title(self, page_id: const.PageID) -> str:
        """Get the title of a Page.

        Args:
            page_id (PageID): The ID of the Page to get the title of.

        Returns:
            str: The title of the Page.
        """
        return self.get_page(page_id).PAGE_TITLE.value
