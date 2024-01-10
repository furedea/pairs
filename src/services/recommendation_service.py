"""This module provides the service for generating game recommendations using OpenAI's GPT-3 model."""
import openai

from models import model


def generate_recommended_text(
    genre_model: model.Genre,
    price_model: model.Price,
    hardware_model: model.Hardware,
    game_format_model: model.GameFormat,
    world_view_model: model.WorldView,
    detail_model: model.Detail,
) -> str | None:
    """Generates a game recommendation based on user preferences using OpenAI's GPT-3 model.

    This function takes in the user's preferences for genre, price range, hardware, game format, world view,
    and additional details.
    It then uses these preferences to generate a game recommendation using OpenAI's GPT-3 model.

    Args:
        genre_model (model.Genre): The user's preferred game genre.
        price_model (model.Price): The user's preferred price range for the game.
        hardware_model (model.Hardware): The hardware available to the user.
        game_format_model (model.GameFormat): The user's preferred game format.
        world_view_model (model.WorldView): The user's preferred world view for the game.
        detail_model (model.Detail): Any additional details or preferences provided by the user.

    Returns:
        str | None: A string containing the recommended game, or None if a recommendation could not be generated.
    """
    response = openai.OpenAI().chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=[
            {
                "role": "system",
                "content": "あなたはゲームの推薦をする人です。ユーザーの好みに合ったゲームを推薦してください。",
            },
            {
                "role": "user",
                "content": f"""
                    ジャンル: {genre_model.genre}
                    値段: {price_model.price}
                    ハードウェア: {hardware_model.hardware}
                    ゲーム形式: {game_format_model.game_format}
                    世界観: {world_view_model.world_view}
                    詳細: {detail_model.detail}

                    以下の形式でゲームの推薦をお願いします:
                    推薦ゲーム: [ゲームタイトル]

                    概要: [簡潔なゲーム説明]

                    あなたの要望とのマッチング: このゲームは[ユーザーの要望]に対して[マッチングポイント]を提供します。

                    ユーザーレビュー: [レビューの抜粋]

                    購入/プレイ方法: [購入/プレイ方法に関する情報]
                    """,
            },
        ],
    )
    return response.choices[0].message.content
