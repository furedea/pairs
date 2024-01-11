"""Module for the Account Information Page.

This module contains the AccountInfoPage class. This class is responsible for rendering the account information page
and handling the user interactions on this page.
"""
from typing import ClassVar

import sqlalchemy
import streamlit as st

import session
from models import account, const
from pages.utils import streamlit_util
from services import account_repository


class AccountInfoPage:
    """Class for the Account Information Page.

    This class is responsible for rendering the account information page,
    and handling the user interactions on this page.
    """

    PAGE_ID: ClassVar[const.PageID] = const.PageID.ACCOUNT_INFO
    PAGE_TITLE: ClassVar[const.PageTitle] = const.PageTitle.ACCOUNT_INFO

    __slots__ = ("__session_manager", "__account_repository")

    def __init__(
        self,
        session_manager: session.SessionManager,
        engine: sqlalchemy.Engine,
    ) -> None:
        self.__session_manager = session_manager
        self.__account_repository = account_repository.AccountRepository(engine)

    def render(self) -> None:
        """Render the account information page.

        This method displays the account information page and handles the user interactions on this page.
        """
        st.title(self.PAGE_TITLE.value)

        with streamlit_util.login_required(self.__session_manager) as user_id:
            if user_id is None:
                return

        account_model: account.Account | None = self.__account_repository.fetch(user_id)
        if account_model is None:
            st.error("予期せぬエラーが発生しました: アカウントが存在しません")
            return

        with st.container(border=True):
            st.text(f"ユーザーID: {account_model.user_id}")
            st.text(f"年齢: {account_model.age}")
            st.text(f"性別: {account_model.sex}")

        st.button("検索履歴", on_click=lambda: self.__session_manager.set_page_id(const.PageID.HISTORY))
        st.button(
            label="アカウント削除",
            on_click=lambda: self.__session_manager.set_page_id(const.PageID.DELETE),
        )
        st.button(
            label="検索ページに戻る",
            on_click=lambda: self.__session_manager.set_page_id(const.PageID.RECOMMEND),
        )
