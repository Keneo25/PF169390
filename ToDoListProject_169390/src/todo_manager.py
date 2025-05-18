from src.task import Task
from src.file_manager import FileManager
from src.todo_status import TaskStatus, is_valid_status


class TodoManager:
    """
    Klasa zarządzająca listą zadań w aplikacji Todo.
    Odpowiada za dodawanie, usuwanie, edycję i zmianę statusu zadań.
    Zapewnia również trwałość danych poprzez zapisywanie zmian do pliku.
    """

    def __init__(self, file_path="todo_tasks.txt"):
        self.file_manager = FileManager(file_path)
        self.tasks = self.file_manager.load_tasks()

    def add_task(self, title, description=""):
        """Dodaje nowe zadanie do listy.

        Args:
            title (str): Tytuł nowego zadania
            description (str, optional): Opis zadania. Domyślnie pusty string

        Returns:
            Task: Utworzony obiekt zadania

        Raises:
            ValueError: Gdy tytuł zadania jest pusty
        """
        if not title:
            raise ValueError("Tytuł zadania nie może być pusty")

        new_task = Task(title, description)
        self.tasks.append(new_task)
        self._save_changes()
        return new_task

    def delete_task(self, task_index):
        """Usuwa zadanie z listy.

        Args:
            task_index (int): Indeks zadania do usunięcia

        Returns:
            bool: True jeśli zadanie zostało usunięte, False w przypadku błędu
        """
        try:
            if 0 <= task_index < len(self.tasks):
                del self.tasks[task_index]
                self._save_changes()
                return True
            return False
        except Exception as e:
            print(f"Błąd podczas usuwania zadania: {e}")
            return False

    def edit_task(self, task_index, title=None, description=None):
        """Edytuje istniejące zadanie.

        Args:
            task_index (int): Indeks zadania do edycji
            title (str, optional): Nowy tytuł zadania
            description (str, optional): Nowy opis zadania

        Returns:
            bool: True jeśli zadanie zostało zaktualizowane, False w przypadku błędu
        """
        try:
            if 0 <= task_index < len(self.tasks):
                self.tasks[task_index].update_details(title, description)
                self._save_changes()
                return True
            return False
        except Exception as e:
            print(f"Błąd podczas edycji zadania: {e}")
            return False

    def change_task_status(self, task_index, new_status):
        """Zmienia status zadania.

        Args:
            task_index (int): Indeks zadania, którego status ma być zmieniony
            new_status (TaskStatus lub str): Nowy status zadania

        Returns:
            bool: True jeśli status został zmieniony, False w przypadku błędu

        Raises:
            ValueError: Gdy zadanie ma już podany status
            IndexError: Gdy indeks zadania jest nieprawidłowy
        """
        try:
            if 0 <= task_index < len(self.tasks):

                if isinstance(new_status, str) and is_valid_status(new_status):
                    new_status = TaskStatus(new_status.lower())

                current_task = self.tasks[task_index]
                if current_task.status == new_status:
                    raise ValueError(f"Zadanie ma już status {new_status.value}")

                if isinstance(new_status, TaskStatus):
                    current_task.change_status(new_status)
                    self._save_changes()
                    return True
                return False
            else:
                raise IndexError("Nieprawidłowy indeks zadania")
        except (ValueError, IndexError) as e:
            print(f"Błąd podczas zmiany statusu zadania: {e}")
            return False
        except Exception as e:
            print(f"Nieoczekiwany błąd: {e}")
            return False

    def get_tasks(self):
        """Zwraca listę wszystkich zadań.

        Returns:
            list: Lista wszystkich zadań
        """
        return self.tasks

    def _save_changes(self):
        """Zapisuje zmiany w liście zadań do pliku.

        Aktualizuje plik z zadaniami po każdej operacji modyfikującej listę zadań.
        """
        self.file_manager.save_tasks(self.tasks)


def get_tasks_by_status(todo_manager, status):
    """Zwraca zadania o określonym statusie.

    Args:
        todo_manager (TodoManager): Instancja menedżera zadań
        status (TaskStatus lub str): Status zadań do wyszukania

    Returns:
        list: Lista zadań o podanym statusie
    """
    if not isinstance(status, TaskStatus):
        try:
            status = TaskStatus(status.lower())
        except ValueError:
            return []

    return [task for task in todo_manager.get_tasks() if task.status == status]
