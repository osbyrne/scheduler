from functions import tasks_from_constraints, generate_adjacency_matrix, display_adjacency_matrix, generate_predecessor_matrix, display_predecessor_matrix, check_for_cycle, check_negative_edge, display_ranks, getRank, display_tasks_with_words
import os
from typing import List


def run_all():
    files = os.listdir("src/constraints")
    for file in files:
        Tasks = tasks_from_constraints(f"src/constraints/{file}")

        print(file)
        display_tasks_with_words(Tasks)
        print("\n")

        ajdacencyMatrix: List[List[int]] = generate_adjacency_matrix(Tasks)
        print("adjacency matrix:")
        display_adjacency_matrix(ajdacencyMatrix)
        print("\n")

        predecessorMatrix: List[List[int]] = generate_predecessor_matrix(Tasks)
        print("predecessor matrix:")
        display_predecessor_matrix(predecessorMatrix)
        print("\n")

        hasCycles: bool = check_for_cycle(ajdacencyMatrix)
        print("table has cycles: (true is bad)", hasCycles)

        hasNegativeEdge: bool = check_negative_edge(ajdacencyMatrix)
        print("table has a negative edge: (true is bad)", hasNegativeEdge)

        print("\n")

        if not hasCycles and not hasNegativeEdge:
            display_ranks(getRank(Tasks))
            print("\n")

""" copilot input:
create a CLI
- ask the user to chose a file from the constraints folder or quit
- verify user input
- propose options to the user, including:
    - display the tasks with words
    - display the adjacency matrix
    - display the predecessor matrix
    - check for cycles
    - check for negative edges
    - display the ranks, only if there are no cycles and no negative edges
    - chose another task (and go back to previous screen)
"""
def main():
    while True:
        # Ask the user to choose a file or quit
        print("Choose a file from the constraints folder or enter 'quit' to exit:")
        print("0. Run all options for all files")
        files = os.listdir("src/constraints")
        for i, file in enumerate(files):
            print(f"{i+1}. {file}")
        choice = input("Enter your choice: ")
        
        # Verify user input
        if choice == "quit":
            break
        elif not choice.isdigit() or int(choice) < 1 or int(choice) > len(files):
            print("Invalid choice. Please try again.")
            continue
        
        # Load tasks from the chosen file
        chosen_file = files[int(choice) - 1]
        tasks = tasks_from_constraints(f"src/constraints/{chosen_file}")
        
        while True:
            # Propose options to the user
            print("\nOptions:")
            print("1. Display tasks with words")
            print("2. Display adjacency matrix")
            print("3. Display predecessor matrix")
            print("4. Check for cycles")
            print("5. Check for negative edges")
            if not check_for_cycle(generate_adjacency_matrix(tasks)) and not check_negative_edge(generate_adjacency_matrix(tasks)):
                print("6. Display ranks")
            print("7. Choose another file")
            print("8. Quit")
            option = input("Enter your option: ")
            
            # Verify user input
            if not option.isdigit() or int(option) < 1 or int(option) > 8:
                print("Invalid option. Please try again.")
                continue
            
            # Perform the chosen option
            option = int(option)
            if option == 0:
                run_all()
            elif option == 1:
                display_tasks_with_words(tasks)
            elif option == 2:
                display_adjacency_matrix(generate_adjacency_matrix(tasks))
            elif option == 3:
                display_predecessor_matrix(generate_predecessor_matrix(tasks))
            elif option == 4:
                has_cycles = check_for_cycle(generate_adjacency_matrix(tasks))
                print("Table has cycles: (True is bad)", has_cycles)
            elif option == 5:
                has_negative_edge = check_negative_edge(generate_adjacency_matrix(tasks))
                print("Table has a negative edge: (True is bad)", has_negative_edge)
            elif option == 6:
                if not check_for_cycle(generate_adjacency_matrix(tasks)) and not check_negative_edge(generate_adjacency_matrix(tasks)):
                    display_ranks(getRank(tasks))
            elif option == 7:
                break
            elif option == 8:
                return

if __name__ == "__main__":
    main()