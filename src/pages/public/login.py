"""Module for the Login Page.

This module includes the LoginPage class, which manages the login functionality of the application.
"""
import pydantic
import sqlalchemy
import streamlit as st

import session
from models import const, model
from services import user_repository


class LoginPage:
    """Class for managing the login page.

    This class is responsible for rendering the login page and managing
    the user interactions on this page.
    """

    __slots__ = ("__session_manager", "__user_repository", "title")

    def __init__(
        self,
        session_manager: session.SessionManager,
        engine: sqlalchemy.Engine,
    ) -> None:
        self.__session_manager = session_manager
        self.__user_repository = user_repository.UserRepository(engine)
        self.title = const.PageTitle.LOGIN.value

    def render(self) -> None:
        """Render the login page.

        This method checks if the user is already logged in. If not, it renders the login form.
        """
        st.title(self.title)

        if self.__session_manager.is_user_logged_in():
            return

        with st.form(key="login_form"):
            user_id = st.text_input("ユーザーID")
            password = st.text_input("パスワード", type="password")
            if st.form_submit_button("ログイン"):
                # TODO(kaito): 例外処理の最適化
                try:
                    user_id = model.UserID(user_id=user_id)
                    password = model.Password(password=password)
                    self.__login(user_id, password)
                except (pydantic.ValidationError, AttributeError):
                    st.error("ユーザーIDまたはパスワードが違います")

        st.button(
            label="アカウント登録",
            on_click=lambda: self.__session_manager.set_page_id(const.PageID.REGISTER.name),
        )

    def __login(self, user_id: model.UserID, password: model.Password) -> None:
        """Handles the login process when the login button is clicked.
        It leverages the UserRepository to validate the user's credentials.

        Args:
            user_id (model.UserID): The unique identifier of the user.
            password (model.Password): The password provided by the user. This is not hashed.
        """
        if not self.__user_repository.login(user_id, password):
            st.error("ユーザーIDまたはパスワードが違います")
            return

        self.__session_manager.set_user_id(user_id)
        st.sidebar.success("ログインに成功しました")
        st.rerun()
