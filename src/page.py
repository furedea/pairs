"""Module for managing multiple pages in a Streamlit application.

This module includes the PageController class which is responsible for managing
the functionality of multiple pages in a Streamlit application. It provides methods for
initializing the application, handling user logout, and rendering the sidebar page.
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

    __slots__ = ("__session_manager", "__pages")

    def __init__(self, session_manager: session.SessionManager, engine: sqlalchemy.Engine) -> None:
        """Initialize the MultiPageApp class.

        Args:
            session_manager (SessionManager): Streamlit session manager.
        """
        self.__session_manager = session_manager
        self.__pages = page_model.PageFactory(session_manager, engine)

    def render(self) -> None:
        """Render the side page in the app.

        This method renders the side page in the app. If the user is logged in,
        it also shows a logout button.
        """
        with st.sidebar:
            st.image("img/pairs_icon.png")
            st.title("ゲーム推薦アプリ「Pairs」")

            page_id: const.PageIDLiteral | None = st.container(border=True).radio(
                label="ページ一覧",
                options=self.__pages.page_ids,
                format_func=self.__pages.get_page_title,
                key=const.SessionKey.PAGE_ID.name,
            )
            if page_id is None:
                st.error("ページが見つかりませんでした")

            if (user_id_model := self.__session_manager.get_user_id()) is None:
                st.text("ログインしていません")
            else:
                st.text(f"ユーザID: {user_id_model.user_id}")
                st.button("ログアウト", on_click=self.__logout)

            st.caption(
                "画像: スーパーロゴデザイナ「ロゴ作る君」(https://chat.openai.com/g/g-nPanZDwQ5-suparogodezaina-rogozuo-rujun)"
            )
        self.__pages.get_page(page_id).render()

    def __logout(self) -> None:
        """Logout when logout button clicks.

        This method logs out the user when the logout button is clicked.
        """
        self.__session_manager.set_user_id(None)
        self.__session_manager.set_page_id(const.PageID.LOGIN.name)
