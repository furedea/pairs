"""This module is for the Register Account Page.

The RegisterPage class in this module is responsible for rendering
the registration page and managing the user interactions on this page.
"""
from typing import ClassVar

import pydantic
import sqlalchemy
import streamlit as st

import session
from models import account, const
from pages.utils import streamlit_util
from services import account_repository


class RegisterPage:
    """This class is for the Register Account Page.

    The RegisterPage class is responsible for rendering the registration page and managing
    the user interactions on this page.
    """

    PAGE_ID: ClassVar[const.PageID] = const.PageID.REGISTER
    PAGE_TITLE: ClassVar[const.PageTitle] = const.PageTitle.REGISTER

    __slots__ = ("__session_manager", "__account_repository")

    def __init__(
        self,
        session_manager: session.SessionManager,
        engine: sqlalchemy.Engine,
    ) -> None:
        self.__session_manager = session_manager
        self.__account_repository = account_repository.AccountRepository(engine)

    def render(self) -> None:
        """This method renders the Register Account Page."""
        st.title(self.PAGE_TITLE.value)

        if streamlit_util.is_user_already_logged_in(self.__session_manager):
            return

        with st.form(key="register_form"):
            user_id = st.text_input("ユーザーID(5~20文字)")
            password = st.text_input(label="パスワード(8字以上で英字と数字を含む)", type="password")
            age = st.slider("年齢")
            sex: account.Sex | None = st.selectbox(
                label="性別", options=account.Sex, format_func=lambda sex: sex.value
            )
            if st.form_submit_button("登録"):
                if sex is None:
                    st.error("予期せぬエラーが発生しました: 性別が選択されていません")
                    return
                # TODO(kaito): 例外処理の最適化
                try:
                    user_id = account.UserID(user_id=user_id)
                    password = account.Password(password=password)
                    age = account.Age(age=age)
                    self.__register(user_id, password, age, sex)
                except pydantic.ValidationError as error:
                    st.error(error.errors()[0]["msg"])

        st.button(
            label="ログインページに戻る",
            on_click=lambda: self.__session_manager.set_page_id(const.PageID.LOGIN),
        )

    def __register(
        self, user_id: account.UserID, password: account.Password, age: account.Age, sex: account.Sex
    ) -> None:
        """This method registers a new account when the register button is clicked.

        Args:
            user_id (account.UserID): The user ID.
            password (account.Password): The password.
            age (account.Age): The age.
            sex (account.Sex): The sex.
        """
        # TODO(kaito): 例外処理の最適化
        try:
            self.__account_repository.add(user_id, password, age, sex)
        except sqlalchemy.exc.IntegrityError:
            st.error("ユーザーIDが既に存在しています")
            return

        self.__session_manager.set_user_id(user_id)
        st.sidebar.success("アカウント登録に成功しました")
        st.rerun()
