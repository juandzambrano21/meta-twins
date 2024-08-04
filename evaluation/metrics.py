# evaluation/metrics.py

class EvaluationMetrics:
    def __init__(self):
        self.metrics = {}

    def evaluate(self, task, output, time_taken, resource_usage):
        accuracy = self.calculate_accuracy(task.expected_output, output)
        efficiency = self.calculate_efficiency(time_taken, resource_usage)
        self.metrics[task.description] = {'accuracy': accuracy, 'efficiency': efficiency}

    def calculate_accuracy(self, expected, actual):
        return 1.0 if expected == actual else 0.0

    def calculate_efficiency(self, time_taken, resource_usage):
        return 1.0 / (time_taken + resource_usage)

    def report(self):
        for task, metric in self.metrics.items():
            print(f"Task: {task}, Accuracy: {metric['accuracy']}, Efficiency: {metric['efficiency']}")

