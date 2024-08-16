from aiogram.fsm.state import State, StatesGroup


class ChangeLangugeState(StatesGroup):
    """
        Defines the state for the Change Language process in a finite state machine.

    Attributes:
        change_lang (State): Represents the state where the user is selecting a new language.
    """
    change_lang = State()


__all__ = ("ChangeLangugeState",)
