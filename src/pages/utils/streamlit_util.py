"""This file contains utility functions for the Streamlit application.

It includes functions for checking user login status, creating multiselect widgets, and more.
"""
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from enum import Enum

import streamlit as st

import session
from models import account, const


@contextmanager
def login_required(session_manager: session.SessionManager) -> Iterator[account.UserID | None]:
    """This function checks if the user is logged in.

    If the user is not logged in, it displays an error message and redirects to the login page.

    Args:
        session_manager (session.SessionManager): The session manager.

    Returns:
        Iterator[account.UserID | None]: The user ID if the user is logged in, None otherwise.
    """
    user_id: account.UserID | None = session_manager.get_user_id()
    if user_id is None:
        st.error("ログインしていません")
        st.button("ログインページに戻る", on_click=lambda: session_manager.set_page_id(const.PageID.LOGIN))
        yield None
    else:
        yield user_id


def is_user_already_logged_in(session_manager: session.SessionManager) -> bool:
    """This function checks if the user is already logged in.

    If the user is logged in, it displays an error message and redirects to the search page.

    Args:
        session_manager (session.SessionManager): The session manager.

    Returns:
        bool: True if the user is not logged in, False otherwise.
    """
    if session_manager.get_user_id() is None:
        return False
    st.error("既にログインしています")
    st.button("検索ページに戻る", on_click=lambda: session_manager.set_page_id(const.PageID.RECOMMEND))
    return True


def create_multiselect(label: str, options: Iterable[Enum], placeholder: str = "未選択") -> str:
    """Create a multiselect widget with the given label, options, and placeholder.

    Args:
        label (str): The label for the multiselect widget.
        options (Iterable[Enum]): The options for the multiselect widget.
        placeholder (str): The placeholder for the multiselect widget.

    Returns:
        str: A string of the selected options, separated by commas.
    """
    return ", ".join(
        st.multiselect(
            label=label,
            options=[option.value for option in options],
            placeholder=placeholder,
        )
    )
