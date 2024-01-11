"""Module to manage streamlit.session_state.

This module provides a class to manage the session state in a Streamlit application.
It provides methods to get and set various session state values.
"""
import streamlit as st

from models import account, const


class SessionManager:
    """SessionManager is a class that manages the session state in a Streamlit application.

    It provides methods for manipulating various session state values such as setting and retrieving user ID,
    displaying userbox, and checking if a user is logged in.
    """

    __slots__ = ("__session_state",)

    def __init__(self) -> None:
        """Initializes the SessionManager."""
        self.__session_state = st.session_state
        self.__session_state[const.SessionKey.PAGE_ID.value] = const.PageID.LOGIN
        self.__session_state[const.SessionKey.USER_ID.value] = None

    def set_page_id(self, page: const.PageID) -> None:
        """Sets the current page ID."""
        self.__session_state[const.SessionKey.PAGE_ID.value] = page

    def set_user_id(self, user_id: account.UserID | None) -> None:
        """Sets the current user ID.

        Args:
            user_id (account.UserID | None): The user ID to be set.
        """
        self.__session_state[const.SessionKey.USER_ID.value] = user_id

    def get_user_id(self) -> account.UserID | None:
        """Retrieve the current user ID from the session state.

        Returns:
            account.UserID | None: The current user ID, or None if no user is logged in.
        """
        return self.__session_state[const.SessionKey.USER_ID.value]
