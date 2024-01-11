"""This module contains the HistoryPage class.

The HistoryPage class is responsible for rendering the history page and managing user interactions on this page.
"""
from collections.abc import Sequence
from typing import ClassVar

import sqlalchemy
import streamlit as st

import session
from models import const, history
from pages.utils import streamlit_util
from services import history_repository


class HistoryPage:
    """This class is responsible for rendering the history page and managing user interactions on this page."""

    PAGE_ID: ClassVar[const.PageID] = const.PageID.HISTORY
    PAGE_TITLE: ClassVar[const.PageTitle] = const.PageTitle.HISTORY

    __slots__ = ("__session_manager", "__history_repository")

    def __init__(
        self,
        session_manager: session.SessionManager,
        engine: sqlalchemy.Engine,
    ) -> None:
        self.__session_manager = session_manager
        self.__history_repository = history_repository.HistoryRepository(engine)

    def render(self) -> None:
        """Fetches the user's history and displays it on the page."""
        st.title(self.PAGE_TITLE.value)

        with streamlit_util.login_required(self.__session_manager) as user_id:
            if user_id is None:
                return

        histories: Sequence[history.History] = self.__history_repository.search(user_id)
        if not histories:
            st.error("履歴がありません")
            st.button(
                label="検索ページに戻る",
                on_click=lambda: self.__session_manager.set_page_id(const.PageID.RECOMMEND),
            )
            return
        self.__render_histories(histories)

        st.button("アカウント情報", on_click=lambda: self.__session_manager.set_page_id(const.PageID.ACCOUNT_INFO))

    def __render_histories(self, histories: Sequence[history.History]) -> None:
        """Renders the histories on the page.

        Args:
            histories (Sequence[History]): An iterator of History objects.
        """
        for history_model in histories:
            with st.container(border=True):
                st.text(
                    f"""
                    ジャンル: {history_model.genre}
                    値段: {history_model.price}
                    ハード: {history_model.hardware}
                    ゲーム形式: {history_model.game_format}
                    世界観: {history_model.world_view}
                    詳細: {history_model.detail}
                    おすすめのゲーム: {history_model.recommended_game}
                    """
                )
                if st.button("削除", key=f"delete_{history_model.id}"):
                    self.__history_repository.delete(history_model.id)
                    st.rerun()
