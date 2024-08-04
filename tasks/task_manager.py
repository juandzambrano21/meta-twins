# task_manager.py

class TaskManager:
    def __init__(self, tasks):
        self.tasks = tasks

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task):
        self.tasks.remove(task)

    def get_pending_tasks(self):
        return [task for task in self.tasks if not task.result]
