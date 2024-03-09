


"""
part 1: reading constrain tables

according to the subject:
On each line, the first number is the task number (note that we renamed this attribute to task_id in the class Task, as it is effectively the only identifier of the task in the context of the problem and everything is already a number), 
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
    """
    we assume that:
    - there is no repetition of tasks (whose id is task_id)
    - there are only numbers, no letters

    we note that task_id is unique, so we can use it as key in a dictionary
    we note that task_id is very often equal to the line number, albeit more explicit and forgiving than using the line number as task_id
    """
    tasks = []
    with open(filename) as file:
        for line in file:
            line = line.split()
            task_id = int(line[0])
            duration = int(line[1])
            predecessors = line[2:]
            tasks.append(Task(task_id, duration, *predecessors))

    return tasks

Tasks = tasks_from_constraints("constraints/1.txt")

for task in Tasks:
    print(
        "task number:", task.task_id,
        "task.duration:", task.duration,
        "task.predecessors:", task.predecessors
    )