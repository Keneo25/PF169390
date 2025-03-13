import unittest


class TodoList:
    def __init__(self):
        self.tasks = []
        self.completed_tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def complete_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            self.completed_tasks.append(task)

    def get_active_tasks(self):
        return self.tasks

    def get_completed_tasks(self):
        return self.completed_tasks



class TestTodoList(unittest.TestCase):
    def setUp(self):
        self.todo_list = TodoList()

    def test_add_task(self):
        self.todo_list.add_task("Zadanie 1")  # Task 1
        self.assertIn("Zadanie 1", self.todo_list.get_active_tasks())

    def test_complete_task(self):
        self.todo_list.add_task("Zadanie 1")  # Task 1
        self.todo_list.complete_task("Zadanie 1")  # Task 1
        self.assertNotIn("Zadanie 1", self.todo_list.get_active_tasks())
        self.assertIn("Zadanie 1", self.todo_list.get_completed_tasks())

    def test_get_active_tasks(self):
        self.todo_list.add_task("Zadanie 1")  # Task 1
        self.todo_list.add_task("Zadanie 2")  # Task 2
        self.assertEqual(self.todo_list.get_active_tasks(), ["Zadanie 1", "Zadanie 2"])

    def test_get_completed_tasks(self):
        self.todo_list.add_task("Zadanie 1")  # Task 1
        self.todo_list.complete_task("Zadanie 1")  # Task 1
        self.assertEqual(self.todo_list.get_completed_tasks(), ["Zadanie 1"])

if __name__ == '__main__':
    unittest.main()


