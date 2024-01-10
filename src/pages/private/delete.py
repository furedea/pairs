"""Module for the Account Deletion Page.

This module contains the DeletePage class. This class is responsible for rendering
the account deletion page and managing the user interactions on this page.
"""
import sqlalchemy
import streamlit as st

import session
from models import const, model
from services import account_repository, history_repository


class DeletePage:
    """Class for managing the account deletion page.

    This class is responsible for rendering the account deletion page and managing
    the user interactions on this page.
    """

    __slots__ = ("__session_manager", "__account_repository", "__history_repository", "title")

    def __init__(
        self,
        session_manager: session.SessionManager,
        engine: sqlalchemy.Engine,
    ) -> None:
        self.__session_manager = session_manager
        self.__account_repository = account_repository.AccountRepository(engine)
        self.__history_repository = history_repository.HistoryRepository(engine)
        self.title = const.PageTitle.DELETE.value

    def render(self) -> None:
        """Render the account deletion page."""
        st.title(self.title)

        user_id_model: model.UserID | None = self.__session_manager.get_logged_in_user_id()
        if user_id_model is None:
            return

        st.text(
            f"""
            ユーザーID: {user_id_model.user_id}
            本当に削除しますか?
            """
        )
        st.button(label="削除", on_click=self.__delete, args=(user_id_model,))
        st.button(
            label="アカウント情報に戻る",
            on_click=lambda: self.__session_manager.set_page_id(const.PageID.ACCOUNT_INFO.name),
        )

    def __delete(self, user_id: model.UserID) -> None:
        """Handles the deletion of the user account when the delete button is clicked.

        Args:
            user_id (model.UserID): The unique identifier of the user account to be deleted.
        """
        self.__account_repository.delete(user_id)
        self.__history_repository.delete_all(user_id)
        self.__session_manager.set_user_id(None)
        self.__session_manager.set_page_id(const.PageID.LOGIN.name)
        st.success("アカウントの削除に成功しました")
