"""
This module is responsible for initializing the application and its dependencies.

It contains functions for setting up the database, session, and the application itself.
The database setup utilizes SQLAlchemy and SQLModel.
The session setup involves initializing API client services for authentication, account management, and history.
The application setup involves creating an instance of MultiPageApp.
"""
import sqlalchemy
import sqlalchemy_utils
import sqlmodel
import streamlit as st

import page
import session


def initialize_database(db_user: str, db_password: str, db_host: str, db_port: str, db_name: str) -> sqlalchemy.Engine:
    """Initialize database. This function includes side effects.

    Args:
        db_user (str): Database user.
        db_password (str): Database password.
        db_host (str): Database host.
        db_port (str): Database port.
        db_name (str): Database name.
    Returns:
        sqlalchemy.Engine: Database engine.
    """
    db_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = sqlmodel.create_engine(db_url)
    if not sqlalchemy_utils.database_exists(engine.url):
        sqlalchemy_utils.create_database(engine.url)
    sqlmodel.SQLModel.metadata.create_all(engine)
    return engine


def initialize_app() -> page.PageController:
    """Initialize the app and return the MultiPageApp instance.

    This function initializes the database and the session manager. It also sets the page configuration.
    """
    session_manager = session.SessionManager()
    engine = initialize_database(**st.secrets.db_credentials)
    return page.PageController(session_manager, engine)


def render_app(page_controller: page.PageController) -> None:
    """Render the multi-page app if it exists in the session state."""
    st.set_page_config(
        page_title="Pairs",
        page_icon="img/pairs_icon.png",
        layout="wide",
        menu_items={"About": "基礎PBL成果物"},
    )
    page_controller.render()
