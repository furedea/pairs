"""Main module for the app. This module initializes the app and renders it."""
import streamlit as st

import app
import page


def main() -> None:
    """Main function for initializing and rendering the app."""
    if not st.session_state.get("has_already_started", False):
        st.session_state["has_already_started"] = True
        st.session_state["app"] = app.initialize_app()

    page_controller: page.PageController | None = st.session_state.get("app")
    if page_controller is not None:
        app.render_app(page_controller)


if __name__ == "__main__":
    main()
