"""This module is for the Register Account Page.

The RegisterPage class in this module is responsible for rendering
the registration page and managing the user interactions on this page.
"""
import pydantic
import sqlalchemy
import streamlit as st

import session
from models import const, model
from services import account_repository


class RegisterPage:
    """This class is for the Register Account Page.

    The RegisterPage class is responsible for rendering the registration page and managing
    the user interactions on this page.
    """

    __slots__ = ("__session_manager", "__account_repository", "title")

    def __init__(
        self,
        session_manager: session.SessionManager,
        engine: sqlalchemy.Engine,
    ) -> None:
        self.__session_manager = session_manager
        self.__account_repository = account_repository.AccountRepository(engine)
        self.title = const.PageTitle.REGISTER.value

    def render(self) -> None:
        """This method renders the Register Account Page."""
        st.title(self.title)

        if self.__session_manager.is_user_logged_in():
            return

        with st.form(key="register_form"):
            user_id = st.text_input("ユーザーID(5~20文字)")
            password = st.text_input(label="パスワード(8字以上で英字と数字を含む)", type="password")

            age = st.slider("年齢")
            sex = st.selectbox(label="性別", options=(sex.value for sex in const.Sex))
            if st.form_submit_button("登録"):
                # TODO(kaito): 例外処理の最適化
                try:
                    user_id = model.UserID(user_id=user_id)
                    password = model.Password(password=password)
                    age = model.Age(age=age)
                    self.__register(user_id, password, age, sex)
                except pydantic.ValidationError as error:
                    st.error(error.errors()[0]["msg"])

        st.button(
            label="ログインページに戻る",
            on_click=lambda: self.__session_manager.set_page_id(const.PageID.LOGIN.name),
        )

    def __register(
        self, user_id: model.UserID, password: model.Password, age: model.Age, sex: const.SexLiteral
    ) -> None:
        """This method registers a new account when the register button is clicked.

        Args:
            user_id (model.UserID): The user ID.
            password (model.Password): The password.
            age (model.Age): The age.
            sex (const.SexLiteral): The sex.
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
