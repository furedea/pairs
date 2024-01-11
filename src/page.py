"""This module manages multiple pages in a Streamlit application.

It contains the PageController class that oversees the functionality of various pages in the Streamlit application.
The class provides methods for application initialization, user logout handling, and sidebar page rendering.
"""
import sqlalchemy
import streamlit as st

import session
from models import const, page_model


class PageController:
    """PageController class for managing multiple pages in a Streamlit application.

    This class is responsible for managing the functionality of multiple pages in a Streamlit application.
    It provides methods for initializing the application, handling user logout, and rendering the sidebar page.
    """

    __slots__ = ("__session_manager", "__page_factory")

    def __init__(self, session_manager: session.SessionManager, engine: sqlalchemy.Engine) -> None:
        """Initialize the MultiPageApp class.

        Args:
            session_manager (SessionManager): Streamlit session manager.
        """
        self.__session_manager = session_manager
        self.__page_factory = page_model.PageFactory(session_manager, engine)

    def render(self) -> None:
        """Render the sidebar of the application.

        This method is responsible for rendering the sidebar of the application.
        If the user is authenticated, a logout button is also displayed.
        """
        with st.sidebar:
            st.image("img/pairs_icon.png")
            st.title("ゲーム推薦アプリ「Pairs」")

            page_id: const.PageID | None = st.container(border=True).radio(
                label="ページ一覧",
                options=const.PageID,
                format_func=self.__page_factory.get_page_title,
                key=const.SessionKey.PAGE_ID.value,
            )
            if page_id is None:
                st.error("ページが見つかりませんでした")
                return

            if (user_id_model := self.__session_manager.get_user_id()) is None:
                st.text("ログインしていません")
            else:
                st.text(f"ユーザID: {user_id_model.user_id}")
                st.button("ログアウト", on_click=self.__logout)

            st.caption(
                "画像: スーパーロゴデザイナ「ロゴ作る君」(https://chat.openai.com/g/g-nPanZDwQ5-suparogodezaina-rogozuo-rujun)"
            )

        self.__page_factory.get_page(page_id).render()

    def __logout(self) -> None:
        """Logout when logout button clicks.

        This method logs out the user when the logout button is clicked.
        """
        self.__session_manager.set_user_id(None)
        self.__session_manager.set_page_id(const.PageID.LOGIN)
