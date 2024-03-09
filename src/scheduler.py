


"""
part 1: reading constrain tables

according to the subject:
On each line, the first number is the task number, 
the second is its duration, 
and the other numbers (if present) are the constraints (predecessors)'
"""

class Task:
    def __init__(self, task_number, duration, *args):
        self.task_number = task_number
        self.duration = duration
        self.predecessors = args

    def __str__(self):
        return f"Task number: {self.task_number}, Duration: {self.duration}, Predecessors: {self.predecessors}"

def tasks_from_constraints(filename: str) -> list[Task]:
    tasks = []
    with open(filename) as file:
        for line in file:
            line = line.split()
            task_number = int(line[0])
            duration = int(line[1])
            predecessors = line[2:]
            tasks.append(Task(task_number, duration, *predecessors))

    return tasks

Tasks = tasks_from_constraints("constraints/1.txt")

for task in Tasks:
    print(
        "task number:", task.task_number,
        "task.duration:", task.duration,
        "task.predecessors:", task.predecessors
    )