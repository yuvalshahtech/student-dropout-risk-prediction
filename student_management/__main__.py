"""Module entrypoint for `python -m student_management`."""

from .cli import main


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting... Goodbye.")