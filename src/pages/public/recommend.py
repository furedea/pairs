"""This module is for the Recommend Page.

The RecommendPage class in this module is in charge of rendering
the recommendation page and managing the user interactions on this page.
"""
import pydantic
import sqlalchemy
import streamlit as st

import session
from models import const, model
from services import history_repository, recommendation_service


class RecommendPage:
    """This class is for the Recommend Page.

    The RecommendPage class is in charge of rendering the recommendation page and managing
    the user interactions on this page.
    """

    __slots__ = ("__session_manager", "__history_repository", "title")

    def __init__(
        self,
        session_manager: session.SessionManager,
        engine: sqlalchemy.Engine,
    ) -> None:
        self.__session_manager = session_manager
        self.__history_repository = history_repository.HistoryRepository(engine)
        self.title = const.PageTitle.RECOMMEND.value

    def render(self) -> None:
        """This method renders the Recommend Page.

        The render method is in charge of rendering the recommendation page and managing
        the user interactions on this page.
        """
        st.title(self.title)
        st.header("あなたへのおすすめのゲームを提案します")
        st.subheader("あなたの好みを教えてください(複数選択可)")

        with st.container(border=True):
            genre = ", ".join(
                st.multiselect(
                    label="ジャンル",
                    options=(genre.value for genre in const.Genre),
                    placeholder="未選択",
                )
            )
            low_price, high_price = st.slider("価格", value=(0, 10000), step=1000)
            hardware = ", ".join(
                st.multiselect(
                    label="ハードウェア",
                    options=(hardware.value for hardware in const.Hardware),
                    placeholder="未選択",
                )
            )
            game_format = ", ".join(
                st.multiselect(
                    label="ゲーム形式",
                    options=(game_format.value for game_format in const.GameFormat),
                    placeholder="未選択",
                )
            )
            world_view = ", ".join(
                st.multiselect(
                    label="世界観",
                    options=(world_view.value for world_view in const.WorldView),
                    placeholder="未選択",
                )
            )
            with st.expander("詳細検索"):
                detail = st.text_area(
                    label="詳細(1000字以内)",
                    placeholder="好みの詳細を入力してください(好きなゲームやスペックなど)",
                )

            if st.button("検索"):
                with st.spinner("検索中..."):
                    # TODO(kaito): 例外処理の最適化
                    try:
                        genre = model.Genre(genre=genre)
                        price = model.Price(low_price=low_price, high_price=high_price)
                        hardware = model.Hardware(hardware=hardware)
                        game_format = model.GameFormat(game_format=game_format)
                        world_view = model.WorldView(world_view=world_view)
                        detail = model.Detail(detail=detail)
                        self.__recommend(genre, price, hardware, game_format, world_view, detail)
                    except pydantic.ValidationError as error:
                        st.error(error.errors()[0]["msg"])
                        return

        st.button(
            label="アカウント情報",
            on_click=lambda: self.__session_manager.set_page_id(const.PageID.ACCOUNT_INFO.name),
        )

    def __recommend(
        self,
        genre: model.Genre,
        price: model.Price,
        hardware: model.Hardware,
        game_format: model.GameFormat,
        world_view: model.WorldView,
        detail: model.Detail,
    ) -> None:
        """Generate a game recommendation based on user preferences.

        This method is triggered when the recommend button is clicked. It takes in user preferences
        as parameters and generates a game recommendation accordingly.

        Args:
            genre (model.Genre): Preferred genre of the game.
            price (model.Price): Preferred price range of the game.
            hardware (model.Hardware): Preferred hardware for the game.
            game_format (model.GameFormat): Preferred game format.
            world_view (model.WorldView): Preferred world view of the game.
            detail (model.Detail): Additional details or preferences for the game.
        """
        recommended_text: str | None = recommendation_service.generate_recommended_text(
            genre, price, hardware, game_format, world_view, detail
        )
        if recommended_text is None:
            st.error("予期せぬエラーが発生しました: おすすめのゲームが見つかりませんでした")
            return

        recommended_game = model.RecommendedGame.from_text(recommended_text)
        if user_id := self.__session_manager.get_user_id():
            self.__history_repository.add(
                user_id, genre, price, hardware, game_format, world_view, detail, recommended_game
            )

        st.subheader("おすすめのゲーム")
        st.container(border=True).text(recommended_text)
