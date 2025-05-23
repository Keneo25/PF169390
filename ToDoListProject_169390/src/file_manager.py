import os
from src.task import Task


class FileManager:
    """
    Klasa odpowiedzialna za operacje I/O na plikach z zadaniami.
    Zapewnia zapisywanie i odczytywanie listy zadań.
    """

    def __init__(self, file_path="database_todo.txt"):
        self.file_path = file_path

    def save_tasks(self, tasks):
        """Zapisuje listę zadań do pliku.

        Args:
            tasks (list): Lista obiektów Task do zapisania

        Returns:
            bool: True jeśli zapis się powiódł, False w przypadku błędu
        """
        try:
            with open(self.file_path, "w") as file:
                for task in tasks:
                    file.write(task.to_string() + "\n")
            return True
        except Exception as e:
            print(f"Błąd podczas zapisywania zadań: {e}")
            return False

    def load_tasks(self):
        """Wczytuje zadania z pliku.

        Returns:
            list: Lista obiektów Task wczytanych z pliku,
                  lub pusta lista w przypadku błędu lub braku pliku
        """
        tasks = []

        if not os.path.exists(self.file_path):
            open(self.file_path, "w").close()
            return tasks

        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    if line.strip():
                        try:
                            task = Task.from_string(line)
                            tasks.append(task)
                        except ValueError as e:
                            print(f"Pominięto nieprawidłowe zadanie: {e}")
            return tasks
        except Exception as e:
            print(f"Błąd podczas odczytu zadań: {e}")
            return []
