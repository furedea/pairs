"""This module defines constant values for the application.
It includes several enumerations and literals that are used throughout the application.

Enumerations:
    SessionKey: Defines the keys for different session states in the application.
    PageID: Defines the IDs for different pages in the application.
    PageTitle: Defines the titles for different pages in the application.
    Sex: Defines the options for user's sex.
    Genre: Defines the options for game genres.
    Hardware: Defines the options for game hardware.
    GameFormat: Defines the options for game formats.
    WorldView: Defines the options for game world views.
"""
from enum import Enum, auto


class SessionKey(Enum):
    """Enumeration to define Session keys for streamlit.session_state."""

    PAGE_ID = auto()
    USER_ID = auto()


class PageID(Enum):
    """Enumeration to define Page IDs."""

    LOGIN = auto()
    REGISTER = auto()
    RECOMMEND = auto()
    ACCOUNT_INFO = auto()
    HISTORY = auto()
    DELETE = auto()


class PageTitle(Enum):
    """Enumeration to define Page titles."""

    LOGIN = "ログイン"
    REGISTER = "アカウント登録"
    RECOMMEND = "検索"
    ACCOUNT_INFO = "アカウント情報"
    HISTORY = "検索履歴"
    DELETE = "アカウント削除"


class Genre(Enum):
    """Enumeration to define Genre options."""

    ACTION = "アクション"
    ADVENTURE = "アドベンチャー"
    RPG = "ロールプレイング"
    SHOOTING = "シューティング"
    SIMULATION = "シミュレーション"
    SPORTS = "スポーツ"
    TRIVIA = "トリビア"
    PUZZLE = "パズル"
    MUSIC = "ミュージック"
    RACING = "レース"


class Hardware(Enum):
    """Enumeration to define Hardware options."""

    WINDOWS = "Windows"
    MAC = "Mac"
    IOS = "iOS"
    ANDROID = "Android"
    SWITCH = "Switch"
    PLAY_STATION = "Play Station"


class GameFormat(Enum):
    """Enumeration to define Game Format options."""

    TWO_D = "2D"
    THREE_D = "3D"
    HD2D = "HD2D"
    DOT = "ドット"
    ANIME = "アニメ調"
    REAL = "リアル調"


class WorldView(Enum):
    """Enumeration to define World View options."""

    MODERN = "現代"
    FUTURE = "未来"
    ANCIENT = "古代"
    RECENT = "近代"
    MIDDLE_AGES = "中世"
    FANTASY = "ファンタジー"
    SF = "SF"
    STEAMPUNK = "スチームパンク"
    HORROR = "ホラー"
    BATTLE_ROYALE = "バトルロワイヤル"
