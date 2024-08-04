# simple_math.py

class SimpleMathTool:
    def __init__(self):
        self.description = "Performs basic mathematical operations (addition, subtraction)."

    def run(self, input_data):
        operation = input_data.get("operation")
        num1 = input_data.get("num1")
        num2 = input_data.get("num2")

        if not all([operation, num1, num2]):
            return "Error: Missing input data."

        try:
            num1 = float(num1)
            num2 = float(num2)
        except ValueError:
            return "Error: Invalid input numbers."

        if operation == "add":
            return num1 + num2
        elif operation == "subtract":
            return num1 - num2
        else:
            return "Error: Invalid operation."
