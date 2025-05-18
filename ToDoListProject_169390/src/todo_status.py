from enum import Enum


class TaskStatus(Enum):
    """Enumeracja reprezentująca możliwe statusy zadania.

    Attributes:
        DONE (str): Status oznaczający zadanie zakończone
        PENDING (str): Status oznaczający zadanie oczekujące
        UNFINISHED (str): Status oznaczający zadanie nieukończone
    """

    DONE = "done"
    PENDING = "pending"
    UNFINISHED = "unfinished"


def get_default_status():
    """Zwraca domyślny status dla nowego zadania.

    Returns:
        TaskStatus: Domyślny status (PENDING) dla nowego zadania
    """
    return TaskStatus.PENDING


def is_valid_status(status_name):
    """Sprawdza czy podany tekst to prawidłowy status.

    Args:
        status_name (str): Nazwa statusu do sprawdzenia

    Returns:
        bool: True jeśli status jest prawidłowy, False w przeciwnym razie
    """
    try:
        TaskStatus(status_name.lower())
        return True
    except ValueError:
        return False
