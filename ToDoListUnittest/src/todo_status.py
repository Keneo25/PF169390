from enum import Enum


class TaskStatus(Enum):
    DONE = "done"
    PENDING = "pending"
    UNFINISHED = "unfinished"


def get_default_status():
    """Zwraca domyślny status dla nowego zadania."""
    return TaskStatus.PENDING


def is_valid_status(status_name):
    """Sprawdza czy podany tekst to prawidłowy status."""
    try:
        TaskStatus(status_name.lower())
        return True
    except ValueError:
        return False
