"""Module to manage streamlit.session_state.

This module provides a class to manage the session state in a Streamlit application.
It provides methods to get and set various session state values.
"""
import streamlit as st

from models import const, model


class SessionManager:
    """SessionManager is a class that manages the session state in a Streamlit application.

    It provides methods for manipulating various session state values such as setting and retrieving user ID,
    displaying userbox, and checking if a user is logged in.
    """

    __slots__ = ("__session_state", "engine")

    def __init__(self) -> None:
        """Initializes the SessionManager."""
        self.__session_state = st.session_state
        self.__session_state[const.SessionKey.PAGE_ID.name] = const.PageID.LOGIN.name
        self.__session_state[const.SessionKey.USER_ID.name] = None
        self.__session_state[const.SessionKey.USERBOX.name] = None

    def set_page_id(self, page_id: const.PageIDLiteral) -> None:
        """Sets the current page ID."""
        self.__session_state[const.SessionKey.PAGE_ID.name] = page_id

    def set_user_id(self, user_id: model.UserID | None) -> None:
        """Sets the current user ID.

        Args:
            user_id (str | None): The user ID to set.
        """
        self.__session_state[const.SessionKey.USER_ID.name] = user_id

    def get_user_id(self) -> model.UserID | None:
        """Retrieve the current user ID from the session state.

        Returns:
            model.UserID | None: The current user ID, or None if no user is logged in.
        """
        return self.__session_state[const.SessionKey.USER_ID.name]

    def get_logged_in_user_id(self) -> model.UserID | None:
        """Check if the user is not logged in and display an error message if they are not.

        Returns:
            model.UserID | None: The current user ID, or None if no user is logged in.
        """
        user_id: model.UserID | None = self.get_user_id()
        if user_id is not None:
            return user_id
        st.error("ログインしていません")
        st.button("ログインページに戻る", on_click=lambda: self.set_page_id(const.PageID.LOGIN.name))
        return None

    def is_user_logged_in(self) -> bool:
        """Checks if the user is logged in and displays an error message if they are.

        Returns:
            bool: True if the user is not logged in, False otherwise.
        """
        if self.get_user_id() is None:
            return False
        st.error("既にログインしています")
        st.button("検索ページに戻る", on_click=lambda: self.set_page_id(const.PageID.RECOMMEND.name))
        return True
