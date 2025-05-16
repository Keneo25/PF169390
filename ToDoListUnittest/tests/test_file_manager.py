import unittest
import os
import tempfile
import unittest.mock as mock
from src.file_manager import FileManager
from src.task import Task
from src.todo_status import TaskStatus


class TestFileManager(unittest.TestCase):
    def setUp(self):
        """Przygotowanie danych przed każdym testem."""

        self.temp_file = tempfile.NamedTemporaryFile(delete=False).name
        self.file_manager = FileManager(self.temp_file)

        self.task1 = Task("Zadanie 1", "Opis 1")
        self.task2 = Task("Zadanie 2", "Opis 2", TaskStatus.DONE)
        self.tasks = [self.task1, self.task2]

    def tearDown(self):
        """Sprzątanie po testach."""

        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_save_tasks_empty_list(self):
        """Test zapisania pustej listy zadań."""
        result = self.file_manager.save_tasks([])
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.temp_file))
        with open(self.temp_file, "r") as file:
            content = file.read()
        self.assertEqual(content, "")

    def test_save_tasks_single_task(self):
        """Test zapisania jednego zadania."""
        self.file_manager.save_tasks([self.task1])
        with open(self.temp_file, "r") as file:
            content = file.read().strip()
        expected = self.task1.to_string()
        self.assertEqual(content, expected)

    def test_save_tasks_multiple_tasks(self):
        """Test zapisania wielu zadań."""
        self.file_manager.save_tasks(self.tasks)
        with open(self.temp_file, "r") as file:
            lines = file.readlines()

        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0].strip(), self.task1.to_string())
        self.assertEqual(lines[1].strip(), self.task2.to_string())

    def test_save_tasks_with_error(self):
        """Test zapisania zadań z błędem (nieprawidłowa ścieżka)."""
        invalid_file_manager = FileManager("/nonexistent/directory/file.txt")
        result = invalid_file_manager.save_tasks(self.tasks)
        self.assertFalse(result)

    def test_load_tasks_nonexistent_file(self):
        """Test wczytania zadań z nieistniejącego pliku."""

        nonexistent_file = os.path.join(tempfile.gettempdir(), "nonexistent_file.txt")
        if os.path.exists(nonexistent_file):
            os.remove(nonexistent_file)

        file_manager = FileManager(nonexistent_file)
        tasks = file_manager.load_tasks()

        self.assertTrue(os.path.exists(nonexistent_file))
        self.assertEqual(len(tasks), 0)

        os.remove(nonexistent_file)

    def test_load_tasks_empty_file(self):
        """Test wczytania zadań z pustego pliku."""

        with open(self.temp_file, "w") as file:
            pass

        tasks = self.file_manager.load_tasks()
        self.assertEqual(len(tasks), 0)

    def test_load_tasks_with_valid_data(self):
        """Test wczytania zadań z prawidłowymi danymi."""

        self.file_manager.save_tasks(self.tasks)

        loaded_tasks = self.file_manager.load_tasks()

        self.assertEqual(len(loaded_tasks), 2)
        self.assertEqual(loaded_tasks[0].title, self.task1.title)
        self.assertEqual(loaded_tasks[0].description, self.task1.description)
        self.assertEqual(loaded_tasks[0].status, self.task1.status)
        self.assertEqual(loaded_tasks[1].title, self.task2.title)
        self.assertEqual(loaded_tasks[1].description, self.task2.description)
        self.assertEqual(loaded_tasks[1].status, self.task2.status)

    def test_load_tasks_with_invalid_data(self):
        """Test wczytania zadań z nieprawidłowymi danymi."""

        with open(self.temp_file, "w") as file:
            file.write("Zadanie 1|Opis 1|pending\n")
            file.write("Nieprawidłowe_dane\n")
            file.write("Zadanie 3|Opis 3|invalid_status\n")
            file.write("Zadanie 4|Opis 4|done\n")

        loaded_tasks = self.file_manager.load_tasks()

        self.assertEqual(len(loaded_tasks), 2)
        self.assertEqual(loaded_tasks[0].title, "Zadanie 1")
        self.assertEqual(loaded_tasks[1].title, "Zadanie 4")

    def test_load_tasks_with_empty_lines(self):
        """Test wczytania zadań z pustymi liniami w pliku."""

        with open(self.temp_file, "w") as file:
            file.write("Zadanie 1|Opis 1|pending\n")
            file.write("\n")
            file.write("Zadanie 2|Opis 2|done\n")
            file.write("\n")

        loaded_tasks = self.file_manager.load_tasks()

        self.assertEqual(len(loaded_tasks), 2)

    def test_load_tasks_permission_error(self):
        """Test wczytania zadań z pliku bez uprawnień do odczytu."""

        if os.name != "posix":
            self.skipTest("Test dostępu działa tylko na systemach POSIX")

        self.file_manager.save_tasks(self.tasks)

        try:
            os.chmod(self.temp_file, 0o000)

            loaded_tasks = self.file_manager.load_tasks()

            self.assertEqual(len(loaded_tasks), 0)
        finally:

            os.chmod(self.temp_file, 0o666)

    def test_save_and_load_tasks_with_special_characters(self):
        """Test zapisania i wczytania zadań ze znakami specjalnymi (z wyjątkiem znaku '|')."""

        task_with_special_chars = Task("Zadanie ze znakami !@#$%", "Opis z enterami")
        self.file_manager.save_tasks([task_with_special_chars])

        loaded_tasks = self.file_manager.load_tasks()
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0].title, "Zadanie ze znakami !@#$%")
        self.assertEqual(loaded_tasks[0].description, "Opis z enterami")

    def test_load_tasks_with_unicode_characters(self):
        """Test wczytania zadań z pliku zawierającego proste znaki."""
        task_with_simple_chars = Task("Zadanie specjalne", "Opis specjalny")
        self.file_manager.save_tasks([task_with_simple_chars])

        loaded_tasks = self.file_manager.load_tasks()
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0].title, "Zadanie specjalne")
        self.assertEqual(loaded_tasks[0].description, "Opis specjalny")

    def test_load_tasks_with_multiple_invalid_lines(self):
        """Test wczytania zadań z pliku zawierającego wiele nieprawidłowych linii."""
        with open(self.temp_file, "w") as file:
            file.write("Prawidłowe|Zadanie 1|pending\n")
            file.write("Nieprawidłowa linia\n")
            file.write("Bardzo|nieprawidłowa|linia|z|wieloma|elementami\n")
            file.write("Prawidłowe|Zadanie 2|done\n")
            file.write("Zadanie|bez|właściwego|statusu\n")

        loaded_tasks = self.file_manager.load_tasks()
        self.assertEqual(len(loaded_tasks), 2)
        self.assertEqual(loaded_tasks[0].title, "Prawidłowe")
        self.assertEqual(loaded_tasks[1].title, "Prawidłowe")

    def test_save_tasks_overwrites_previous_content(self):
        """Test, czy zapisanie zadań nadpisuje poprzednią zawartość pliku."""

        self.file_manager.save_tasks(self.tasks)

        single_task = [Task("Nowe zadanie", "Nowy opis")]
        result = self.file_manager.save_tasks(single_task)

        self.assertTrue(result)

        loaded_tasks = self.file_manager.load_tasks()
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0].title, "Nowe zadanie")

    def test_save_tasks_with_very_long_strings(self):
        """Test zapisania zadań z bardzo długimi ciągami znaków."""
        long_title = "A" * 1000
        long_description = "B" * 5000
        task_with_long_strings = Task(long_title, long_description)

        result = self.file_manager.save_tasks([task_with_long_strings])
        self.assertTrue(result)

        loaded_tasks = self.file_manager.load_tasks()
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(len(loaded_tasks[0].title), 1000)
        self.assertEqual(len(loaded_tasks[0].description), 5000)

    def test_load_tasks_from_file_with_strange_line_endings(self):
        """Test wczytania zadań z pliku z różnymi zakończeniami linii."""

        with open(self.temp_file, "wb") as file:
            file.write(b"Zadanie 1|Opis 1|pending\r\n")
            file.write(b"Zadanie 2|Opis 2|done\n")
            file.write(b"Zadanie 3|Opis 3|unfinished\r")

        loaded_tasks = self.file_manager.load_tasks()
        self.assertEqual(len(loaded_tasks), 3)
        self.assertEqual(loaded_tasks[0].title, "Zadanie 1")
        self.assertEqual(loaded_tasks[1].title, "Zadanie 2")
        self.assertEqual(loaded_tasks[2].title, "Zadanie 3")

    def test_load_tasks_with_corrupted_file(self):
        """Test wczytania zadań z uszkodzonego pliku."""

        with open(self.temp_file, "wb") as file:
            file.write(b"\x80\x81\x82Nieprawidlowe\xf0\xf1\xf2dane\x00")

        loaded_tasks = self.file_manager.load_tasks()
        self.assertEqual(len(loaded_tasks), 0)

    def test_save_tasks_with_different_statuses(self):
        """Test zapisania zadań o różnych statusach."""
        tasks = [
            Task("Zadanie 1", "Opis 1", TaskStatus.PENDING),
            Task("Zadanie 2", "Opis 2", TaskStatus.DONE),
            Task("Zadanie 3", "Opis 3", TaskStatus.UNFINISHED),
        ]

        result = self.file_manager.save_tasks(tasks)
        self.assertTrue(result)

        loaded_tasks = self.file_manager.load_tasks()
        self.assertEqual(len(loaded_tasks), 3)
        self.assertEqual(loaded_tasks[0].status, TaskStatus.PENDING)
        self.assertEqual(loaded_tasks[1].status, TaskStatus.DONE)
        self.assertEqual(loaded_tasks[2].status, TaskStatus.UNFINISHED)

    def test_save_and_load_multiple_times(self):
        """Test wielokrotnego zapisywania i wczytywania danych."""

        self.file_manager.save_tasks([self.task1])
        loaded_tasks = self.file_manager.load_tasks()
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0].title, self.task1.title)

        self.file_manager.save_tasks([self.task2])
        loaded_tasks = self.file_manager.load_tasks()
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0].title, self.task2.title)

        self.file_manager.save_tasks(self.tasks)
        loaded_tasks = self.file_manager.load_tasks()
        self.assertEqual(len(loaded_tasks), 2)

    def test_load_tasks_with_unexpected_exception(self):
        """Test obsługi nieoczekiwanego wyjątku podczas wczytywania zadań."""
        original_open = open

        def mocked_open(*args, **kwargs):
            if args[0] == self.temp_file and "r" in args[1]:
                raise Exception("Symulowany nieoczekiwany błąd")
            return original_open(*args, **kwargs)

        try:

            import builtins

            builtins.open = mocked_open

            loaded_tasks = self.file_manager.load_tasks()
            self.assertEqual(len(loaded_tasks), 0)
        finally:

            builtins.open = original_open

    def test_save_tasks_with_unexpected_exception(self):
        """Test obsługi nieoczekiwanego wyjątku podczas zapisywania zadań."""
        original_open = open

        def mocked_open(*args, **kwargs):
            if args[0] == self.temp_file and "w" in args[1]:
                raise Exception("Symulowany nieoczekiwany błąd")
            return original_open(*args, **kwargs)

        try:

            import builtins

            builtins.open = mocked_open

            result = self.file_manager.save_tasks(self.tasks)
            self.assertFalse(result)
        finally:

            builtins.open = original_open

    def test_save_tasks_to_readonly_location(self):
        """Test zapisu do lokalizacji tylko do odczytu."""

        with mock.patch("builtins.open") as mock_open:
            mock_open.side_effect = PermissionError("Brak uprawnień do zapisu")
            result = self.file_manager.save_tasks(self.tasks)

        self.assertFalse(result)
        mock_open.assert_called_once()

    def test_save_tasks_during_disk_full(self):
        """Test zapisu zadań gdy dysk jest pełny."""
        with unittest.mock.patch("builtins.open") as mock_open:

            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.write.side_effect = OSError("Disk full")

            result = self.file_manager.save_tasks(self.tasks)

        self.assertFalse(result)
        self.assertTrue(mock_file.write.called)

    def test_load_tasks_with_file_read_error(self):
        """Test wczytania zadań gdy wystąpi błąd podczas czytania pliku."""

        self.file_manager.save_tasks(self.tasks)

        with unittest.mock.patch("builtins.open") as mock_open:

            def selective_mock(*args, **kwargs):
                if "r" in args[1]:
                    mock_file = unittest.mock.MagicMock()
                    mock_file.__enter__.return_value.readlines.side_effect = IOError(
                        "Błąd odczytu"
                    )
                    return mock_file

                return open(*args, **kwargs)

            mock_open.side_effect = selective_mock

            loaded_tasks = self.file_manager.load_tasks()

        self.assertIsInstance(loaded_tasks, list)
        self.assertEqual(len(loaded_tasks), 0)

    def test_task_file_creation_with_permissions(self):
        """Test tworzenia pliku zadań z określonymi uprawnieniami."""

        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

        with unittest.mock.patch("builtins.open") as mock_open:
            mock_open.return_value.__enter__.return_value = unittest.mock.MagicMock()
            self.file_manager.load_tasks()

        mock_open.assert_any_call(self.temp_file, "w")

    def test_file_manager_with_default_path(self):
        """Test inicjalizacji FileManager z domyślną ścieżką pliku."""
        default_manager = FileManager()

        self.assertEqual(default_manager.file_path, "todo_tasks.txt")
        self.assertIsNot(default_manager.file_path, self.temp_file)
        self.assertIsInstance(default_manager.file_path, str)
