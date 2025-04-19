"""Main entry point to run evolutionary-snake"""
import enum


class GameMode(enum.StrEnum):
    """Enum to define game modes."""
    HUMAN_PLAYER = "human_player"
    TRAINING = "train"
    AI_PLAYER = "ai_player"


def main(
        mode: GameMode,
) -> bool:
    """Main entry point to run evolutionary-snake."""
    if mode == GameMode.HUMAN_PLAYER:
        print("Human player starting...")
    elif mode == GameMode.TRAINING:
        print("Training starting...")
    elif mode == GameMode.AI_PLAYER:
        print("AI player starting...")
    else:
        print(f"Invalid mode {mode} given")
    return True


if __name__ == "__main__":
    game_mode = GameMode.HUMAN_PLAYER
    print("=" * 20, f" running mode: {game_mode} ", "=" * 20)
    main(mode=game_mode)
