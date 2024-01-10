"""This module contains the HistoryPage class.

The HistoryPage class is responsible for rendering the history page and managing user interactions on this page.
"""
from collections.abc import Sequence

import sqlalchemy
import streamlit as st

import session
from models import const, model
from services import history_repository


class HistoryPage:
    """This class is responsible for rendering the history page and managing user interactions on this page."""

    __slots__ = ("__session_manager", "__history_repository", "title")

    def __init__(
        self,
        session_manager: session.SessionManager,
        engine: sqlalchemy.Engine,
    ) -> None:
        self.__session_manager = session_manager
        self.__history_repository = history_repository.HistoryRepository(engine)
        self.title = const.PageTitle.HISTORY.value

    def render(self) -> None:
        """Fetches the user's history and displays it on the page."""
        st.title(self.title)

        user_id: model.UserID | None = self.__session_manager.get_logged_in_user_id()
        if user_id is None:
            return

        histories: Sequence[model.History] = self.__history_repository.search(user_id)
        if not histories:
            st.error("履歴がありません")
            st.button(
                label="検索ページに戻る",
                on_click=lambda: self.__session_manager.set_page_id(const.PageID.RECOMMEND.name),
            )
            return
        self.__render_histories(histories)

        st.button(
            "アカウント情報", on_click=lambda: self.__session_manager.set_page_id(const.PageID.ACCOUNT_INFO.name)
        )

    def __render_histories(self, histories: Sequence[model.History]) -> None:
        """Renders the histories on the page.

        Args:
            histories (Sequence[History]): An iterator of History objects.
        """
        for history in histories:
            with st.container(border=True):
                st.text(
                    f"""
                    ジャンル: {history.genre}
                    値段: {history.price}
                    ハード: {history.hardware}
                    ゲーム形式: {history.game_format}
                    世界観: {history.world_view}
                    詳細: {history.detail}
                    おすすめのゲーム: {history.recommended_game}
                    """
                )
                if st.button("削除", key=f"delete_{history.id}"):
                    self.__history_repository.delete(history.id)
                    st.rerun()
