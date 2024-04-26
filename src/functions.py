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
    def __init__(self, task_id: int, duration: int, *args):
        self.task_id: int = task_id
        self.duration: int = duration
        self.predecessors = args
        self.successors: List[int] = []
        self.earliest_start: int = 0
        self.latest_start: int = 0
        self.rank: int = 0

    def __str__(self):
        return f"Task {self.task_id}: duration={self.duration}, predecessors={self.predecessors}, successors={self.successors}, earliest_start={self.earliest_start}, latest_start={self.latest_start}, rank={self.rank}"


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

    # Append task_id to the list of successors for each task
    for task in tasks:
        for predecessor in task.predecessors:
            predecessor_id = int(predecessor)
            tasks[predecessor_id - 1].successors.append(task.task_id) 
    
            """ Why - 1 ?
            GitHub Copilot used /explain
                Python uses zero-based indexing : the first element of a list has an index of 0.
                predecessor_id represents the task ID of the predecessor task. 
                Since the task IDs start from 1, subtracting 1 from predecessor_id ensures that we access the correct index in the tasks list.
            """

    # we add the fictitious tasks alpha labeled 0
    tasks.append(Task(0, 0))

    # we add the fictitious tasks omega labeled N+1
    last_tasks: List[int] = []
    for task in tasks:
        if task.successors == []:
            last_tasks.append(task.task_id)
    tasks.append(Task(len(tasks) + 1, 0, last_tasks))

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
    
    for task in tasks:
        task_id = task.task_id
        successors = task.successors

        for successor in successors:
            successor_id = int(successor)
            adjacency_matrix[task_id - 1][successor_id - 1] = 1

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


    return False
def check_for_cycle(tasks: List[Task]) -> bool:
    """
    This function checks for cycles in the task graph using depth-first search (DFS).
    It starts from each unvisited task and explores its successors.
    If a successor has already been visited, it means there is a cycle in the graph.
    The function returns True if a cycle is found, and False otherwise.
    """
    visited = set()  # Initialize visited set to track visited tasks
    
    def dfs(task):
        if task.task_id in visited:
            return True  # Cycle detected
        
        visited.add(task.task_id)
        
        for successor_id in task.successors:
            successor = tasks[successor_id - 1]  # Task IDs are 1-based
            if dfs(successor):
                return True
        
        visited.remove(task.task_id)  # Remove the task from visited set after DFS traversal
        return False
    
    # Start DFS from each unvisited task
    for task in tasks:
        if task.task_id not in visited:
            if dfs(task):
                return True  # Cycle detected
    
    return False  # No cycles found

def check_negative_edge(tasks: List[Task]) -> bool:
    # This function checks for negative edges in the given adjacency matrix.
    # It returns True if a negative edge is found, and False otherwise.

    for task in tasks:
        if task.duration < 0:
            return True
    return False


def getRank(tasks: List[Task], task_id: int) -> None:
    predecessors_ranks: List[int] = []
    for predecessor in tasks[task_id - 1].predecessors:
        if isinstance(predecessor, list):
            for id in predecessor:
                predecessors_ranks.append(tasks[int(id)-1].rank)
        else:
            predecessors_ranks.append(tasks[int(predecessor)-1].rank)

    if tasks[task_id-1].predecessors == []:
        return 0
    else:
        return max(predecessors_ranks) + 1 if predecessors_ranks else 0

def setRank(tasks: List[Task]) -> None:
    for task in tasks:
        task.rank = getRank(tasks, task.task_id)