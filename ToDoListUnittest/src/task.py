from src.todo_status import TaskStatus, get_default_status


class Task:
    """
    Klasa reprezentująca pojedyncze zadanie w aplikacji Todo.
    Przechowuje informacje o tytule, opisie i statusie zadania.
    Umożliwia aktualizację właściwości zadania oraz konwersję między
    obiektami zadań a reprezentacją tekstową.
    """

    def __init__(self, title, description="", status=None):
        self.title = title
        self.description = description
        self.status = status if status else get_default_status()

    def change_status(self, new_status):
        """Zmienia status zadania."""
        if isinstance(new_status, TaskStatus):
            self.status = new_status
            return True
        return False

    def update_details(self, title=None, description=None):
        """Aktualizuje szczegóły zadania."""
        if title:
            self.title = title
        if description is not None:
            self.description = description

    def to_string(self):
        """Konwertuje zadanie do formatu string dla zapisu do pliku."""
        return f"{self.title}|{self.description}|{self.status.value}"

    @classmethod
    def from_string(cls, task_string):
        """Tworzy obiekt zadania z tekstu wczytanego z pliku."""
        try:
            parts = task_string.strip().split("|")
            if len(parts) != 3:
                raise ValueError("Nieprawidłowy format zadania")

            title, description, status_value = parts
            status = TaskStatus(status_value)

            return cls(title, description, status)
        except Exception as e:
            raise ValueError(f"Nie można utworzyć zadania: {e}")
