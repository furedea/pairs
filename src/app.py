"""
This module is responsible for initializing the application and its dependencies.

It contains functions for setting up the database, session, and the application itself.
The database setup utilizes SQLAlchemy and SQLModel.
The session setup involves initializing API client services for authentication, account management, and history.
The application setup involves creating an instance of MultiPageApp.
"""
from pathlib import Path

import sqlalchemy
import sqlmodel
import streamlit as st

import page
import session


def initialize_database(db_dir_path: str, sqlite_url: str) -> sqlalchemy.Engine:
    """Initialize database. This function includes side effects.

    Args:
        db_dir_path (str): The path to the directory where the database file will be stored.
        sqlite_url (str): The URL to the SQLite database.

    Returns:
        sqlalchemy.Engine: Database engine.
    """
    Path(__file__).parent.parent.joinpath(db_dir_path).mkdir(exist_ok=True)
    engine = sqlmodel.create_engine(sqlite_url)
    sqlmodel.SQLModel.metadata.create_all(engine)
    return engine


def initialize_app() -> page.PageController:
    """Initialize the app and return the MultiPageApp instance.

    This function initializes the database and the session manager. It also sets the page configuration.
    """
    session_manager = session.SessionManager()
    engine = initialize_database("db", "sqlite:///db/pairs.db")
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
