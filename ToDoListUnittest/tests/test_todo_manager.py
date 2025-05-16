import unittest
import os
import tempfile
import unittest.mock
from src.todo_manager import TodoManager, get_tasks_by_status
from src.todo_status import TaskStatus


class TestTodoManager(unittest.TestCase):
    def setUp(self):
        """Przygotowanie danych przed każdym testem."""

        self.temp_file = tempfile.NamedTemporaryFile(delete=False).name
        self.todo_manager = TodoManager(self.temp_file)

    def tearDown(self):
        """Sprzątanie po testach."""

        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_add_task(self):
        """Test dodawania zadania."""
        task = self.todo_manager.add_task("Nowe zadanie", "Opis zadania")
        self.assertIsNotNone(task)
        self.assertEqual(task.title, "Nowe zadanie")
        self.assertEqual(task.description, "Opis zadania")
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(len(self.todo_manager.get_tasks()), 1)

    def test_add_task_empty_title(self):
        """Test dodawania zadania z pustym tytułem."""
        with self.assertRaises(ValueError):
            self.todo_manager.add_task("")

    def test_add_task_without_description(self):
        """Test dodawania zadania bez opisu."""
        task = self.todo_manager.add_task("Tylko tytuł")
        self.assertEqual(task.description, "")

    def test_delete_task_valid_index(self):
        """Test usuwania zadania o prawidłowym indeksie."""
        self.todo_manager.add_task("Zadanie 1")
        self.todo_manager.add_task("Zadanie 2")
        result = self.todo_manager.delete_task(0)
        self.assertTrue(result)
        self.assertEqual(len(self.todo_manager.get_tasks()), 1)
        self.assertEqual(self.todo_manager.get_tasks()[0].title, "Zadanie 2")

    def test_delete_task_invalid_index(self):
        """Test usuwania zadania o nieprawidłowym indeksie."""
        self.todo_manager.add_task("Zadanie 1")
        result = self.todo_manager.delete_task(5)
        self.assertFalse(result)
        self.assertEqual(len(self.todo_manager.get_tasks()), 1)

    def test_delete_task_negative_index(self):
        """Test usuwania zadania o ujemnym indeksie."""
        self.todo_manager.add_task("Zadanie 1")
        result = self.todo_manager.delete_task(-1)
        self.assertFalse(result)
        self.assertEqual(len(self.todo_manager.get_tasks()), 1)

    def test_edit_task_valid_index(self):
        """Test edycji zadania o prawidłowym indeksie."""
        self.todo_manager.add_task("Stary tytuł", "Stary opis")
        result = self.todo_manager.edit_task(0, "Nowy tytuł", "Nowy opis")
        self.assertTrue(result)
        task = self.todo_manager.get_tasks()[0]
        self.assertEqual(task.title, "Nowy tytuł")
        self.assertEqual(task.description, "Nowy opis")

    def test_edit_task_only_title(self):
        """Test edycji tylko tytułu zadania."""
        self.todo_manager.add_task("Stary tytuł", "Opis")
        result = self.todo_manager.edit_task(0, "Nowy tytuł")
        self.assertTrue(result)
        task = self.todo_manager.get_tasks()[0]
        self.assertEqual(task.title, "Nowy tytuł")
        self.assertEqual(task.description, "Opis")

    def test_edit_task_only_description(self):
        """Test edycji tylko opisu zadania."""
        self.todo_manager.add_task("Tytuł", "Stary opis")
        result = self.todo_manager.edit_task(0, None, "Nowy opis")
        self.assertTrue(result)
        task = self.todo_manager.get_tasks()[0]
        self.assertEqual(task.title, "Tytuł")
        self.assertEqual(task.description, "Nowy opis")

    def test_edit_task_invalid_index(self):
        """Test edycji zadania o nieprawidłowym indeksie."""
        self.todo_manager.add_task("Zadanie")
        result = self.todo_manager.edit_task(5, "Nowy tytuł")
        self.assertFalse(result)

    def test_change_task_status_valid_index_enum(self):
        """Test zmiany statusu zadania używając enum TaskStatus."""
        self.todo_manager.add_task("Zadanie")
        result = self.todo_manager.change_task_status(0, TaskStatus.DONE)
        self.assertTrue(result)
        self.assertEqual(self.todo_manager.get_tasks()[0].status, TaskStatus.DONE)

    def test_change_task_status_valid_index_string(self):
        """Test zmiany statusu zadania używając stringa."""
        self.todo_manager.add_task("Zadanie")
        result = self.todo_manager.change_task_status(0, "done")
        self.assertTrue(result)
        self.assertEqual(self.todo_manager.get_tasks()[0].status, TaskStatus.DONE)

    def test_change_task_status_invalid_string(self):
        """Test zmiany statusu zadania na nieprawidłowy string."""
        self.todo_manager.add_task("Zadanie")
        result = self.todo_manager.change_task_status(0, "nieistniejący_status")
        self.assertFalse(result)
        self.assertEqual(self.todo_manager.get_tasks()[0].status, TaskStatus.PENDING)

    def test_change_task_status_same_status(self):
        """Test zmiany statusu zadania na ten sam co obecny."""
        self.todo_manager.add_task("Zadanie")
        result = self.todo_manager.change_task_status(0, TaskStatus.PENDING)
        self.assertFalse(result)

    def test_change_task_status_invalid_index(self):
        """Test zmiany statusu zadania o nieprawidłowym indeksie."""
        self.todo_manager.add_task("Zadanie")
        result = self.todo_manager.change_task_status(5, TaskStatus.DONE)
        self.assertFalse(result)

    def test_get_tasks_empty(self):
        """Test pobrania pustej listy zadań."""
        tasks = self.todo_manager.get_tasks()
        self.assertEqual(len(tasks), 0)

    def test_get_tasks_multiple(self):
        """Test pobrania listy z wieloma zadaniami."""
        self.todo_manager.add_task("Zadanie 1")
        self.todo_manager.add_task("Zadanie 2")
        self.todo_manager.add_task("Zadanie 3")
        tasks = self.todo_manager.get_tasks()
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].title, "Zadanie 1")
        self.assertEqual(tasks[1].title, "Zadanie 2")
        self.assertEqual(tasks[2].title, "Zadanie 3")

    def test_get_tasks_by_status_enum(self):
        """Test pobrania zadań o określonym statusie używając enum."""

        self.todo_manager.add_task("Zadanie 1")
        self.todo_manager.add_task("Zadanie 2")
        self.todo_manager.change_task_status(0, TaskStatus.DONE)

        done_tasks = get_tasks_by_status(self.todo_manager, TaskStatus.DONE)
        self.assertEqual(len(done_tasks), 1)
        self.assertEqual(done_tasks[0].title, "Zadanie 1")

        pending_tasks = get_tasks_by_status(self.todo_manager, TaskStatus.PENDING)
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0].title, "Zadanie 2")

    def test_get_tasks_by_status_string(self):
        """Test pobrania zadań o określonym statusie używając stringa."""

        self.todo_manager.add_task("Zadanie 1")
        self.todo_manager.add_task("Zadanie 2")
        self.todo_manager.change_task_status(0, "done")

        done_tasks = get_tasks_by_status(self.todo_manager, "done")
        self.assertEqual(len(done_tasks), 1)
        self.assertEqual(done_tasks[0].title, "Zadanie 1")

    def test_get_tasks_by_status_invalid_string(self):
        """Test pobrania zadań o nieprawidłowym statusie."""
        self.todo_manager.add_task("Zadanie 1")
        tasks = get_tasks_by_status(self.todo_manager, "nieistniejący_status")
        self.assertEqual(len(tasks), 0)

    def test_persistence_between_instances(self):
        """Test sprawdzający czy dane są zachowywane między instancjami."""

        self.todo_manager.add_task("Zadanie do zapisania")

        new_manager = TodoManager(self.temp_file)

        tasks = new_manager.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Zadanie do zapisania")

    def test_get_tasks_by_status_with_empty_manager(self):
        """Test funkcji get_tasks_by_status na pustym menedżerze zadań."""

        tasks = get_tasks_by_status(self.todo_manager, TaskStatus.PENDING)
        self.assertListEqual(tasks, [])

        tasks = get_tasks_by_status(self.todo_manager, "done")
        self.assertListEqual(tasks, [])

    @unittest.mock.patch("src.todo_manager.is_valid_status")
    def test_change_task_status_invalid_status_validation(self, mock_is_valid):
        """Test zmiany statusu zadania gdy walidacja zwraca False."""

        self.todo_manager.add_task("Zadanie testowe")

        mock_is_valid.return_value = False

        result = self.todo_manager.change_task_status(0, "nieprawidłowy")

        self.assertFalse(result)
        self.assertEqual(self.todo_manager.get_tasks()[0].status, TaskStatus.PENDING)
        mock_is_valid.assert_called_once_with("nieprawidłowy")

    @unittest.mock.patch("src.todo_manager.FileManager")
    def test_todo_manager_file_error_handling(self, mock_file_manager_class):
        """Test obsługi błędów przy inicjalizacji TodoManager z problematycznym FileManager."""

        mock_file_manager = unittest.mock.MagicMock()
        mock_file_manager.load_tasks.return_value = []
        mock_file_manager_class.return_value = mock_file_manager

        manager = TodoManager("błędna_ścieżka.txt")

        self.assertIsInstance(manager, TodoManager)
        self.assertIsInstance(manager.tasks, list)
        self.assertEqual(len(manager.tasks), 0)

        mock_file_manager_class.assert_called_once_with("błędna_ścieżka.txt")

    def test_change_task_status_unexpected_exception(self):
        """Test obsługi nieoczekiwanego wyjątku przy zmianie statusu zadania."""

        self.todo_manager.add_task("Zadanie testowe")

        original_task = self.todo_manager.tasks[0]
        mock_task = unittest.mock.MagicMock()
        mock_task.status = TaskStatus.PENDING
        mock_task.change_status.side_effect = Exception("Nieoczekiwany błąd")
        self.todo_manager.tasks[0] = mock_task

        result = self.todo_manager.change_task_status(0, TaskStatus.DONE)

        self.assertFalse(result)
        mock_task.change_status.assert_called_once_with(TaskStatus.DONE)

        self.todo_manager.tasks[0] = original_task

    def test_add_task_persistence(self):
        """Test czy dodane zadanie jest rzeczywiście zapisywane do pliku."""

        task = self.todo_manager.add_task("Zadanie testowe")

        new_manager = TodoManager(self.temp_file)

        self.assertEqual(len(new_manager.get_tasks()), 1)
        self.assertEqual(new_manager.get_tasks()[0].title, "Zadanie testowe")
        self.assertIsNot(new_manager.get_tasks()[0], task)

    @unittest.mock.patch("src.todo_manager.FileManager.save_tasks")
    def test_save_changes_error_handling(self, mock_save_tasks):
        """Test obsługi błędów przy zapisywaniu zmian."""

        mock_save_tasks.return_value = False

        task = self.todo_manager.add_task("Zadanie testowe")

        self.assertEqual(len(self.todo_manager.get_tasks()), 1)
        mock_save_tasks.assert_called_once()

    def test_get_tasks_by_status_with_none_argument(self):
        """Test funkcji get_tasks_by_status z argumentem None."""

        self.todo_manager.add_task("Zadanie 1")
        self.todo_manager.add_task("Zadanie 2")

        with self.assertRaises(AttributeError):
            get_tasks_by_status(self.todo_manager, None)
