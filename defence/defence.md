---
marp: true
---
---
marp: true
---
                    Oscar Byrne / Romain Ferrigo / Sofiane Kherraf
#                       Task Scheduler Presentation
 

Welcome to the Task Scheduler Presentation!

We will present to you the result of our project aimed at implementing scheduling in python using our knowledge of graph theory


                            

---
# Task Class

    
    class Task:
        def __init__(self, task_id, duration, *args):
            self.task_id = task_id
            self.duration = duration
            self.predecessors = args
            self.successors = []

        def __str__(self):
            return f"Task number: {self.task_id}, Duration: {self.duration}, Predecessors: {self.predecessors}"
---
# tasks_from_constraints Function

    

    def tasks_from_constraints(filename: str) -> list[Task]:
        """
        Reads the constraints from a file and returns a list of Task objects.

        Args:
        - filename (str): The path to the file containing constraints.

        Returns:
        - List[Task]: A list of Task objects representing the tasks parsed from the file.
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
        
        # Add fictitious tasks alpha labeled 0 and omega labeled N+1
        tasks.append(Task(0, 0))
        tasks.append(Task(len(tasks) + 1, 0))

        return tasks

---
# Displaying the task 
    
    def display_tasks_with_words(tasks: List[Task]) -> None:
    """
    Displays the tasks with their IDs, durations, and predecessors.

    Args:
    - tasks (List[Task]): A list of Task objects.

    Returns:
    - None
    """
    print("id, duration, predecessors")
    for task in tasks:
        print(task.task_id, "     ", task.duration, "     ", task.predecessors)




---
# The Adjacency Matrix

    def generate_adjacency_matrix(tasks: List[Task]) -> List[List[int]]:
        """
        Generates the adjacency matrix representing the task dependencies.

        Args:
        - tasks (List[Task]): A list of Task objects.

        Returns:
        - List[List[int]]: The adjacency matrix representing task dependencies.
        """
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

---
# Predecessor Matrix
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
        """
        Displays the predecessor matrix representing task dependencies.

        Args:
        - predecessor_matrix (List[List[int]]): The predecessor matrix to display.

        Returns:
        - None
        """
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
    
---

# Cycle Detection in Graph

## Function: `has_cycles`

    This function checks if there are any cycles in the task graph, which would indicate a scheduling conflict or impossibility.

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
 ---
# Thank You for Listening!

Feel free to ask any questions or start a discussion!

---
