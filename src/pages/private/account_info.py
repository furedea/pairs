"""Module for the Account Information Page.

This module contains the AccountInfoPage class. This class is responsible for rendering the account information page
and handling the user interactions on this page.
"""
import sqlalchemy
import streamlit as st

import session
from models import const, model
from services import account_repository


class AccountInfoPage:
    """Class for the Account Information Page.

    This class is responsible for rendering the account information page,
    and handling the user interactions on this page.
    """

    __slots__ = ("__session_manager", "__account_repository", "title")

    def __init__(
        self,
        session_manager: session.SessionManager,
        engine: sqlalchemy.Engine,
    ) -> None:
        self.__session_manager = session_manager
        self.__account_repository = account_repository.AccountRepository(engine)
        self.title = const.PageTitle.ACCOUNT_INFO.value

    def render(self) -> None:
        """Render the account information page.

        This method displays the account information page and handles the user interactions on this page.
        """
        st.title(self.title)

        user_id: model.UserID | None = self.__session_manager.get_logged_in_user_id()
        if user_id is None:
            return

        account: model.Account | None = self.__account_repository.fetch(user_id)
        if account is None:
            st.error("予期せぬエラーが発生しました: アカウントが存在しません")
            return

        with st.container(border=True):
            st.text(f"ユーザーID: {account.user_id}")
            st.text(f"年齢: {account.age}")
            st.text(f"性別: {account.sex}")

        st.button("検索履歴", on_click=lambda: self.__session_manager.set_page_id(const.PageID.HISTORY.name))
        st.button(
            label="アカウント削除",
            on_click=lambda: self.__session_manager.set_page_id(const.PageID.DELETE.name),
        )
        st.button(
            label="検索ページに戻る",
            on_click=lambda: self.__session_manager.set_page_id(const.PageID.RECOMMEND.name),
        )
