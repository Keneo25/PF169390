import unittest
import unittest.mock
from src.task import Task
from src.todo_status import TaskStatus


class TestTask(unittest.TestCase):
    def setUp(self):
        """Przygotowanie danych przed każdym testem."""
        self.title = "Przykładowe zadanie"
        self.description = "Opis przykładowego zadania"
        self.task = Task(self.title, self.description)

    def test_task_initialization(self):
        """Test poprawnej inicjalizacji zadania."""
        self.assertEqual(self.task.title, self.title)
        self.assertEqual(self.task.description, self.description)
        self.assertEqual(self.task.status, TaskStatus.PENDING)

    def test_task_initialization_with_status(self):
        """Test inicjalizacji zadania z określonym statusem."""
        task = Task(self.title, self.description, TaskStatus.DONE)
        self.assertEqual(task.status, TaskStatus.DONE)

    def test_change_status_valid(self):
        """Test zmiany statusu na prawidłowy."""
        result = self.task.change_status(TaskStatus.DONE)
        self.assertTrue(result)
        self.assertEqual(self.task.status, TaskStatus.DONE)

    def test_change_status_invalid(self):
        """Test zmiany statusu na nieprawidłowy."""
        initial_status = self.task.status
        result = self.task.change_status("nieistniejący_status")
        self.assertFalse(result)
        self.assertEqual(self.task.status, initial_status)

    def test_update_details_title_only(self):
        """Test aktualizacji tylko tytułu zadania."""
        new_title = "Nowy tytuł"
        self.task.update_details(title=new_title)
        self.assertEqual(self.task.title, new_title)
        self.assertEqual(self.task.description, self.description)

    def test_update_details_description_only(self):
        """Test aktualizacji tylko opisu zadania."""
        new_description = "Nowy opis"
        self.task.update_details(description=new_description)
        self.assertEqual(self.task.title, self.title)
        self.assertEqual(self.task.description, new_description)

    def test_update_details_both(self):
        """Test aktualizacji zarówno tytułu jak i opisu zadania."""
        new_title = "Nowy tytuł"
        new_description = "Nowy opis"
        self.task.update_details(new_title, new_description)
        self.assertEqual(self.task.title, new_title)
        self.assertEqual(self.task.description, new_description)

    def test_to_string(self):
        """Test konwersji zadania do formatu string."""
        expected = f"{self.title}|{self.description}|pending"
        self.assertEqual(self.task.to_string(), expected)

    def test_from_string_valid(self):
        """Test tworzenia zadania z prawidłowego formatu string."""
        task_string = "Tytuł|Opis|done"
        task = Task.from_string(task_string)
        self.assertEqual(task.title, "Tytuł")
        self.assertEqual(task.description, "Opis")
        self.assertEqual(task.status, TaskStatus.DONE)

    def test_from_string_invalid_format(self):
        """Test tworzenia zadania z nieprawidłowego formatu string (za mało elementów)."""
        task_string = "Tytuł|Opis"
        with self.assertRaises(ValueError):
            Task.from_string(task_string)

    def test_from_string_invalid_format_too_many(self):
        """Test tworzenia zadania z nieprawidłowego formatu string (za dużo elementów)."""
        task_string = "Tytuł|Opis|done|extra"
        with self.assertRaises(ValueError):
            Task.from_string(task_string)

    def test_from_string_invalid_status(self):
        """Test tworzenia zadania z nieprawidłowym statusem."""
        task_string = "Tytuł|Opis|nieprawidłowy_status"
        with self.assertRaises(ValueError):
            Task.from_string(task_string)

    def test_from_string_empty(self):
        """Test tworzenia zadania z pustego stringa."""
        task_string = ""
        with self.assertRaises(ValueError):
            Task.from_string(task_string)

    def test_empty_title_initialization(self):
        """Test inicjalizacji zadania z pustym tytułem."""
        task = Task("")
        self.assertEqual(task.title, "")

    def test_none_description_initialization(self):
        """Test inicjalizacji zadania z None jako opis."""
        task = Task("Tytuł", None)
        self.assertEqual(task.description, None)

    def test_update_details_none_values(self):
        """Test aktualizacji z None jako wartości."""
        self.task.update_details(title=None, description=None)
        self.assertEqual(self.task.title, self.title)
        self.assertEqual(self.task.description, self.description)

    def test_to_string_with_special_chars(self):
        """Test konwersji do stringa zadania ze znakami specjalnymi."""
        task = Task("Tytuł | ze znakiem", "Opis | ze znakiem")
        result = task.to_string()
        self.assertEqual(result, "Tytuł | ze znakiem|Opis | ze znakiem|pending")

    def test_from_string_with_empty_description(self):
        """Test tworzenia zadania z pustym opisem."""
        task_string = "Tytuł||done"
        task = Task.from_string(task_string)
        self.assertEqual(task.title, "Tytuł")
        self.assertEqual(task.description, "")
        self.assertEqual(task.status, TaskStatus.DONE)

    def test_from_string_with_edge_cases(self):
        """Test tworzenia zadania z tekstu zawierającego znaki specjalne."""
        task_string = "Tytuł ze znakami !@#$%|Opis z&^*|pending"
        task = Task.from_string(task_string)
        self.assertEqual(task.title, "Tytuł ze znakami !@#$%")
        self.assertEqual(task.description, "Opis z&^*")
        self.assertEqual(task.status, TaskStatus.PENDING)

    @unittest.mock.patch("src.task.get_default_status")
    def test_task_initialization_default_status(self, mock_get_default):
        """Test, czy zadanie używa funkcji get_default_status."""
        mock_get_default.return_value = TaskStatus.UNFINISHED

        task = Task("Testowe zadanie")

        self.assertEqual(task.status, TaskStatus.UNFINISHED)

    def test_task_string_representation(self):
        """Test reprezentacji tekstowej zadania."""

        task_str = str(self.task)
        self.assertIsInstance(task_str, str)
        self.assertGreater(len(task_str), 0)

    def test_task_equality(self):
        """Test porównania dwóch zadań o tych samych parametrach."""
        task1 = Task("Zadanie", "Opis", TaskStatus.PENDING)
        task2 = Task("Zadanie", "Opis", TaskStatus.PENDING)

        self.assertIsNot(task1, task2)

        self.assertEqual(task1.title, task2.title)
        self.assertEqual(task1.description, task2.description)
        self.assertEqual(task1.status, task2.status)

    def test_change_status_same_status(self):
        """Test zmiany statusu na ten sam co obecnie."""
        initial_status = self.task.status
        result = self.task.change_status(initial_status)
        self.assertTrue(result)
        self.assertEqual(self.task.status, initial_status)

    def test_update_details_empty_title(self):
        """Test aktualizacji tytułu na pusty string."""
        task = Task("Przykładowe zadanie", "Opis")

        task.update_details(title="")

        self.assertEqual(task.title, "Przykładowe zadanie")
        self.assertEqual(task.description, "Opis")

    def test_to_string_with_complex_values(self):
        """Test konwersji zadania z złożonymi wartościami do formatu string."""
        title_with_chars = "Zadanie | ze znakiem |"
        desc_with_chars = "Opis | ze znakiem |"
        task = Task(title_with_chars, desc_with_chars)

        expected = f"{title_with_chars}|{desc_with_chars}|pending"
        self.assertEqual(task.to_string(), expected)

        with self.assertRaises(ValueError):

            Task.from_string(task.to_string())

    def test_from_string_with_malformed_input(self):
        """Test tworzenia zadania z niepoprawnego wejścia."""
        with self.assertRaises(ValueError):
            Task.from_string(None)

    def test_from_string_with_exception_in_status_creation(self):
        """Test obsługi wyjątku przy tworzeniu statusu."""
        with unittest.mock.patch("src.task.TaskStatus") as mock_status:
            mock_status.side_effect = Exception("Testowy wyjątek")
            with self.assertRaises(ValueError) as context:
                Task.from_string("Tytuł|Opis|pending")
            self.assertIn("Nie można utworzyć zadania", str(context.exception))

    def test_task_initialization_with_invalid_status(self):
        """Test inicjalizacji zadania z nieprawidłowym typem statusu."""

        task = Task("Tytuł", "Opis", "invalid_status")

        self.assertEqual(task.status, "invalid_status")

    def test_change_status_with_none(self):
        """Test zmiany statusu na None."""
        initial_status = self.task.status
        result = self.task.change_status(None)
        self.assertFalse(result)
        self.assertEqual(self.task.status, initial_status)
