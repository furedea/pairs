"""This module provides the service for generating game recommendations using OpenAI's GPT-3.5 model."""
import openai

from models import history


def generate_recommended_text(
    genre_model: history.Genre,
    price_model: history.Price,
    hardware_model: history.Hardware,
    game_format_model: history.GameFormat,
    world_view_model: history.WorldView,
    detail_model: history.Detail,
) -> str | None:
    """Generates a game recommendation based on user preferences using OpenAI's GPT-3.5 model.

    This function takes in the user's preferences for genre, price range, hardware, game format, world view,
    and additional details.
    It then uses these preferences to generate a game recommendation using OpenAI's GPT-3.5 model.

    Args:
        genre_model (history.Genre): The user's preferred game genre.
        price_model (history.Price): The user's preferred price range for the game.
        hardware_model (history.Hardware): The hardware available to the user.
        game_format_model (history.GameFormat): The user's preferred game format.
        world_view_model (history.WorldView): The user's preferred world view for the game.
        detail_model (history.Detail): Any additional details or preferences provided by the user.

    Returns:
        str | None: A string containing the recommended game, or None if a recommendation could not be generated.
    """
    response = openai.OpenAI().chat.completions.create(
        model="gpt-3.5-turbo-1106",  # gpt-4-1106-preview takes longer
        messages=[
            {
                "role": "system",
                "content": "あなたはゲームの推薦をする人です。ユーザーの好みに合ったゲームを推薦してください。",
            },
            {
                "role": "user",
                "content": f"""
                    ユーザーの要望:
                    ジャンル: {genre_model.genre}
                    価格帯: {price_model.price}
                    対応ハードウェア: {hardware_model.hardware}
                    ゲーム形式: {game_format_model.game_format}
                    世界観: {world_view_model.world_view}
                    その他の詳細: {detail_model.detail}

                    出力形式:
                    推薦ゲーム: [ゲームタイトル]
                    概要: [簡潔なゲーム説明]
                    あなたの要望とのマッチング: このゲームは[ユーザーの要望]に対して[マッチングポイント]を提供します。
                    ユーザーレビュー: [レビューの抜粋]
                    購入/プレイ方法: [購入/プレイ方法に関する情報]

                    注記: 条件が不明瞭または限られている場合は、広く人気のあるゲームを推薦してください。
                    """,
            },
        ],
    )
    return response.choices[0].message.content
