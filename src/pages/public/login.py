"""Module for the Login Page.

This module includes the LoginPage class, which manages the login functionality of the application.
"""
from typing import ClassVar

import pydantic
import sqlalchemy
import streamlit as st

import session
from models import account, const
from pages.utils import streamlit_util
from services import user_repository


class LoginPage:
    """Class for managing the login page.

    This class is responsible for rendering the login page and managing
    the user interactions on this page.
    """

    PAGE_ID: ClassVar[const.PageID] = const.PageID.LOGIN
    PAGE_TITLE: ClassVar[const.PageTitle] = const.PageTitle.LOGIN

    __slots__ = ("__session_manager", "__user_repository")

    def __init__(
        self,
        session_manager: session.SessionManager,
        engine: sqlalchemy.Engine,
    ) -> None:
        self.__session_manager = session_manager
        self.__user_repository = user_repository.UserRepository(engine)

    def render(self) -> None:
        """Render the login page.

        This method checks if the user is already logged in. If not, it renders the login form.
        """
        st.title(self.PAGE_TITLE.value)

        if streamlit_util.is_user_already_logged_in(self.__session_manager):
            return

        with st.form(key="login_form"):
            user_id = st.text_input("ユーザーID")
            password = st.text_input("パスワード", type="password")
            if st.form_submit_button("ログイン"):
                # TODO(kaito): 例外処理の最適化
                try:
                    user_id = account.UserID(user_id=user_id)
                    password = account.Password(password=password)
                    self.__login(user_id, password)
                except (pydantic.ValidationError, AttributeError):
                    st.error("ユーザーIDまたはパスワードが違います")

        st.button(
            label="アカウント登録",
            on_click=lambda: self.__session_manager.set_page_id(const.PageID.REGISTER),
        )

    def __login(self, user_id: account.UserID, password: account.Password) -> None:
        """Handles the login process when the login button is clicked.
        It leverages the UserRepository to validate the user's credentials.

        Args:
            user_id (account.UserID): The unique identifier of the user.
            password (account.Password): The password provided by the user. This is not hashed.
        """
        if not self.__user_repository.login(user_id, password):
            st.error("ユーザーIDまたはパスワードが違います")
            return

        self.__session_manager.set_user_id(user_id)
        st.sidebar.success("ログインに成功しました")
        st.rerun()
