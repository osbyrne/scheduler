import os
from typing import List

"""
part 1: reading constrain tables

according to the subject:
On each line,
- the first number is the task number (which we renamed as task_id in the class Task, because it is effectively the only identifier of the task in the context of the problem and everything is already a number),
- the second is its duration,
- and the other numbers (if present) are the constraints (predecessors)'
"""


class Task:
    def __init__(self, task_id, duration, *args):
        self.task_id = task_id
        self.duration = duration
        self.predecessors = args

    def __str__(self):
        return f"Task number: {self.task_id}, Duration: {self.duration}, Predecessors: {self.predecessors}"


def tasks_from_constraints(filename: str) -> list[Task]:
    """
    we assume that:
    - there is no repetition of tasks in the contraints table (whose id is task_id)
    - there are only numbers, no letters

    we note that task_id is unique, so we can use it as key in a dictionary
    we note that task_id is very often equal to the line number, but we won't use this assumption
    """
    tasks: List[Task] = []
    with open(filename) as file:
        for line in file:
            line = line.split()
            task_id = int(line[0])
            duration = int(line[1])
            predecessors = line[2:]
            tasks.append(Task(task_id, duration, *predecessors))

    # we add the fictitious tasks alpha labeled 0
    tasks.append(Task(task_id=0, duration=0, predecessors=[0]))

    # we add the fictitious tasks omega labeled N+1
    tasks.append(Task(task_id=len(tasks) + 1, duration=0, predecessors=[0]))

    return tasks


def display_tasks_with_words(tasks: List[Task]) -> None:
    print("id, duration, predecessors")
    for task in tasks:
        print(task.task_id, "     ", task.duration, "     ", task.predecessors)


def generate_adjacency_matrix(tasks: List[Task]) -> List[List[int]]:
    num_tasks = len(tasks)
    adjacency_matrix = [[0] * num_tasks for _ in range(num_tasks)]

    for task in tasks:
        task_id = task.task_id
        predecessors = task.predecessors

        for predecessor in predecessors:
            predecessor_id = int(predecessor)
            adjacency_matrix[task_id - 1][predecessor_id - 1] = 1

    return adjacency_matrix


def display_adjacency_matrix(adjacency_matrix: List[List[int]]) -> None:
    num_tasks = len(adjacency_matrix)

    # Print column headers
    print("   ", end="")
    for i in range(1, num_tasks + 1):
        print(f"Task {i}  ", end="")
    print()

    # Print matrix
    for i in range(num_tasks):
        print(f"Task {i+1}  ", end="")
        for j in range(num_tasks):
            print(f"{adjacency_matrix[i][j]}       ", end="")
        print()


def generate_predecessor_matrix(tasks: List[Task]) -> List[List[int]]:
    num_tasks = len(tasks)
    predecessor_matrix = [[0] * num_tasks for _ in range(num_tasks)]

    for task in tasks:
        task_id = task.task_id
        predecessors = task.predecessors

        for predecessor in predecessors:
            predecessor_id = int(predecessor)
            predecessor_matrix[task_id - 1][predecessor_id - 1] = 1

    return predecessor_matrix


def display_predecessor_matrix(predecessor_matrix: List[List[int]]) -> None:
    num_tasks = len(predecessor_matrix)

    # Print column headers
    print("   ", end="")
    for i in range(1, num_tasks + 1):
        print(f"Task {i}  ", end="")
    print()

    # Print matrix
    for i in range(num_tasks):
        print(f"Task {i+1}  ", end="")
        for j in range(num_tasks):
            print(f"{predecessor_matrix[i][j]}       ", end="")
        print()


def check_for_cycle(adjacency_matrix: List[List[int]]) -> bool:
    # This function checks for cycles in the given adjacency matrix.
    # It uses a depth-first search (DFS) algorithm to traverse the graph.
    # The algorithm starts from each task and explores its neighbors.
    # If a neighbor has already been visited, it means there is a cycle in the graph.
    # The function returns True if a cycle is found, and False otherwise.

    num_tasks = len(adjacency_matrix)

    for i in range(num_tasks):
        visited = [False] * num_tasks
        stack = [i]
        visited[i] = True

        while stack:
            current_task = stack.pop()
            for j in range(num_tasks):
                if adjacency_matrix[current_task][j] == 1:
                    if visited[j]:
                        return True
                    stack.append(j)
                    visited[j] = True
    return False


files = os.listdir("src/constraints")
for file in files:
    Tasks = tasks_from_constraints(f"src/constraints/{file}")

    print(file)
    display_tasks_with_words(Tasks)
    print("\n")

    ajdacencyMatrix: List[List[int]] = generate_adjacency_matrix(Tasks)
    print("adjacency matrix:")
    display_adjacency_matrix(generate_adjacency_matrix(Tasks))
    print("\n")

    predecessorMatrix: List[List[int]] = generate_predecessor_matrix(Tasks)
    print("predecessor matrix:")
    display_predecessor_matrix(generate_predecessor_matrix(Tasks))
    print("\n")

    print("table has cycles:", check_for_cycle(ajdacencyMatrix))
    print("\n")
