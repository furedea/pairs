"""This module is for the Recommend Page.

The RecommendPage class in this module is in charge of rendering
the recommendation page and managing the user interactions on this page.
"""
from typing import ClassVar

import pydantic
import sqlalchemy
import streamlit as st

import session
from models import const, history
from pages.utils import streamlit_util
from services import history_repository, recommendation_service


class RecommendPage:
    """This class is for the Recommend Page.

    The RecommendPage class is in charge of rendering the recommendation page and managing
    the user interactions on this page.
    """

    PAGE_ID: ClassVar[const.PageID] = const.PageID.RECOMMEND
    PAGE_TITLE: ClassVar[const.PageTitle] = const.PageTitle.RECOMMEND

    __slots__ = ("__session_manager", "__history_repository")

    def __init__(
        self,
        session_manager: session.SessionManager,
        engine: sqlalchemy.Engine,
    ) -> None:
        self.__session_manager = session_manager
        self.__history_repository = history_repository.HistoryRepository(engine)

    def render(self) -> None:
        """This method renders the Recommend Page.

        The render method is in charge of rendering the recommendation page and managing
        the user interactions on this page.
        """
        st.title(self.PAGE_TITLE.value)
        st.header("あなたへのおすすめのゲームを提案します")
        st.subheader("あなたの好みを教えてください(複数選択可)")

        with st.container(border=True):
            genre = streamlit_util.create_multiselect("ジャンル", const.Genre)
            low_price, high_price = st.slider("価格", value=(0, 10000), step=1000)
            hardware = streamlit_util.create_multiselect("ハードウェア", const.Hardware)
            game_format = streamlit_util.create_multiselect("ゲーム形式", const.GameFormat)
            world_view = streamlit_util.create_multiselect("世界観", const.WorldView)
            with st.expander("詳細検索"):
                detail = st.text_area(
                    label="詳細(1000字以内)",
                    placeholder="好みの詳細を入力してください(好きなゲームやスペックなど)",
                )

            if st.button("検索"):
                with st.spinner("検索中..."):
                    # TODO(kaito): 例外処理の最適化
                    try:
                        genre = history.Genre(genre=genre)
                        price = history.Price(low_price=low_price, high_price=high_price)
                        hardware = history.Hardware(hardware=hardware)
                        game_format = history.GameFormat(game_format=game_format)
                        world_view = history.WorldView(world_view=world_view)
                        detail = history.Detail(detail=detail)
                        self.__recommend(genre, price, hardware, game_format, world_view, detail)
                    except pydantic.ValidationError as error:
                        st.error(error.errors()[0]["msg"])
                        return

        st.button(
            label="アカウント情報",
            on_click=lambda: self.__session_manager.set_page_id(const.PageID.ACCOUNT_INFO),
        )

    def __recommend(
        self,
        genre: history.Genre,
        price: history.Price,
        hardware: history.Hardware,
        game_format: history.GameFormat,
        world_view: history.WorldView,
        detail: history.Detail,
    ) -> None:
        """Generate a game recommendation based on user preferences.

        This method is triggered when the recommend button is clicked. It takes in user preferences
        as parameters and generates a game recommendation accordingly.

        Args:
            genre (history.Genre): Preferred genre of the game.
            price (history.Price): Preferred price range of the game.
            hardware (history.Hardware): Preferred hardware for the game.
            game_format (history.GameFormat): Preferred game format.
            world_view (history.WorldView): Preferred world view of the game.
            detail (history.Detail): Additional details or preferences for the game.
        """
        recommended_text: str | None = recommendation_service.generate_recommended_text(
            genre, price, hardware, game_format, world_view, detail
        )
        if recommended_text is None:
            st.error("予期せぬエラーが発生しました: おすすめのゲームが見つかりませんでした")
            return

        try:
            recommended_game = history.RecommendedGame.from_text(recommended_text)
        except ValueError as error:
            st.error(error)
            return
        if user_id := self.__session_manager.get_user_id():
            self.__history_repository.add(
                user_id, genre, price, hardware, game_format, world_view, detail, recommended_game
            )

        st.subheader("おすすめのゲーム")
        st.container(border=True).text(recommended_text)
