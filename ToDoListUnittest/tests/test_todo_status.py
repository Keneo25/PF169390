import unittest
import unittest.mock
from src.todo_status import TaskStatus, get_default_status, is_valid_status


class TestTaskStatus(unittest.TestCase):
    def test_task_status_values(self):
        """Test wartości enumeracji TaskStatus."""
        self.assertEqual(TaskStatus.DONE.value, "done")
        self.assertEqual(TaskStatus.PENDING.value, "pending")
        self.assertEqual(TaskStatus.UNFINISHED.value, "unfinished")

    def test_task_status_equality(self):
        """Test równości obiektów TaskStatus."""
        self.assertEqual(TaskStatus.DONE, TaskStatus.DONE)
        self.assertNotEqual(TaskStatus.DONE, TaskStatus.PENDING)
        self.assertNotEqual(TaskStatus.PENDING, TaskStatus.UNFINISHED)

    def test_get_default_status(self):
        """Test funkcji get_default_status."""
        self.assertEqual(get_default_status(), TaskStatus.PENDING)
        self.assertIsInstance(get_default_status(), TaskStatus)

    def test_is_valid_status_valid(self):
        """Test funkcji is_valid_status dla prawidłowych wartości."""
        self.assertTrue(is_valid_status("done"))
        self.assertTrue(is_valid_status("DONE"))
        self.assertTrue(is_valid_status("pending"))
        self.assertTrue(is_valid_status("PENDING"))
        self.assertTrue(is_valid_status("unfinished"))
        self.assertTrue(is_valid_status("UNFINISHED"))

    def test_is_valid_status_invalid(self):
        """Test funkcji is_valid_status dla nieprawidłowych wartości."""
        self.assertFalse(is_valid_status("invalid"))
        self.assertFalse(is_valid_status(""))
        self.assertFalse(is_valid_status("completed"))
        self.assertFalse(is_valid_status("in_progress"))

    def test_create_task_status_from_string(self):
        """Test tworzenia obiektu TaskStatus ze stringa."""
        self.assertEqual(TaskStatus("done"), TaskStatus.DONE)
        self.assertEqual(TaskStatus("pending"), TaskStatus.PENDING)
        self.assertEqual(TaskStatus("unfinished"), TaskStatus.UNFINISHED)

    def test_create_task_status_case_insensitive(self):
        """Test tworzenia obiektu TaskStatus ze stringa z różną wielkością liter."""
        self.assertEqual(TaskStatus("done".upper().lower()), TaskStatus.DONE)
        self.assertEqual(TaskStatus("pending".lower()), TaskStatus.PENDING)
        self.assertEqual(TaskStatus("unfinished".lower()), TaskStatus.UNFINISHED)

    def test_create_task_status_invalid(self):
        """Test tworzenia obiektu TaskStatus z nieprawidłowej wartości."""
        with self.assertRaises(ValueError):
            TaskStatus("invalid")

    def test_is_valid_status_with_whitespace(self):
        """Test funkcji is_valid_status z białymi znakami."""
        self.assertFalse(is_valid_status(" done"))
        self.assertFalse(is_valid_status("done "))
        self.assertFalse(is_valid_status(" pending "))

    def test_is_valid_status_with_none(self):
        """Test funkcji is_valid_status z argumentem None."""
        with self.assertRaises(AttributeError):
            is_valid_status(None)

    def test_is_valid_status_with_numeric(self):
        """Test funkcji is_valid_status z argumentem liczbowym."""
        with self.assertRaises(AttributeError):
            is_valid_status(123)

    def test_create_task_status_invalid_value(self):
        """Test tworzenia obiektu TaskStatus z nieprawidłowej wartości."""
        with self.assertRaises(ValueError):
            TaskStatus("nieprawidłowy_status")

    def test_task_status_comparison(self):
        """Test porównania obiektów TaskStatus."""
        self.assertIsNot(TaskStatus.DONE, TaskStatus.PENDING)
        self.assertIn(TaskStatus.DONE, list(TaskStatus))
        self.assertIn(TaskStatus.PENDING, list(TaskStatus))
        self.assertIn(TaskStatus.UNFINISHED, list(TaskStatus))

    def test_is_valid_status_none_value(self):
        """Test funkcji is_valid_status dla wartości None."""
        with self.assertRaises(AttributeError):
            is_valid_status(None)

    @unittest.mock.patch("src.todo_status.TaskStatus")
    def test_is_valid_status_exception_handling(self, mock_task_status):
        """Test obsługi wyjątków w funkcji is_valid_status."""

        mock_task_status.side_effect = ValueError("Nieoczekiwany błąd")
        self.assertFalse(is_valid_status("pending"))

    def test_task_status_enum_properties(self):
        """Test właściwości enumeracji TaskStatus."""

        self.assertEqual(len(list(TaskStatus)), 3)

        statuses = [status.value for status in TaskStatus]
        self.assertListEqual(
            sorted(statuses), sorted(["done", "pending", "unfinished"])
        )

        for status in TaskStatus:
            self.assertIsInstance(status.value, str)

    @unittest.mock.patch("src.todo_status.TaskStatus")
    def test_get_default_status_behavior(self, mock_task_status):
        """Test zachowania funkcji get_default_status przy różnych implementacjach TaskStatus."""

        pending_mock = unittest.mock.MagicMock()
        pending_mock.name = "PENDING"
        pending_mock.value = "pending"
        mock_task_status.PENDING = pending_mock

        result = get_default_status()
        self.assertEqual(result, pending_mock)
        self.assertEqual(result.value, "pending")

    def test_task_status_immutability(self):
        """Test niezmienności obiektów TaskStatus."""

        with self.assertRaises(AttributeError):
            TaskStatus.DONE = "zmodyfikowana_wartość"

        self.assertEqual(TaskStatus.DONE.value, "done")

        status = TaskStatus.DONE
        status = TaskStatus.PENDING
        self.assertNotEqual(status, TaskStatus.DONE)
        self.assertEqual(status, TaskStatus.PENDING)

    def test_task_status_repr_and_name(self):
        """Test reprezentacji tekstowej i nazwy obiektów TaskStatus."""

        self.assertIn("TaskStatus.DONE", repr(TaskStatus.DONE))
        self.assertIn("TaskStatus.PENDING", repr(TaskStatus.PENDING))

        self.assertEqual(TaskStatus.DONE.name, "DONE")
        self.assertEqual(TaskStatus.PENDING.name, "PENDING")
        self.assertEqual(TaskStatus.UNFINISHED.name, "UNFINISHED")

        self.assertEqual(TaskStatus["DONE"], TaskStatus.DONE)
        self.assertEqual(TaskStatus["PENDING"], TaskStatus.PENDING)

        with self.assertRaises(KeyError):
            TaskStatus["INVALID_NAME"]
