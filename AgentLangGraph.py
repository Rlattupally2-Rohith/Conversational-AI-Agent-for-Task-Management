from langgraph.graph import Graph

# Step 1: Define Task Management Logic
tasks = []

def add_task(task):
    tasks.append({"task": task, "completed": False})
    return f"Added task: {task}"

def complete_task(task_index):
    if 0 <= task_index < len(tasks):
        tasks[task_index]["completed"] = True
        return f"Completed task: {tasks[task_index]['task']}"
    return "Invalid task index."

def list_tasks():
    if not tasks:
        return "No tasks found."
    return "\n".join([f"{i}. {task['task']} - {'Completed' if task['completed'] else 'Pending'}" for i, task in enumerate(tasks)])

def delete_task(task_index):
    if 0 <= task_index < len(tasks):
        deleted_task = tasks.pop(task_index)
        return f"Deleted task: {deleted_task['task']}"
    return "Invalid task index."

# Step 2: Define LangGraph Nodes
def add_task_node(state):
    task = state.get("task")
    return {"response": add_task(task)}

def complete_task_node(state):
    task_index = state.get("task_index")
    return {"response": complete_task(task_index)}

def list_tasks_node(state):
    return {"response": list_tasks()}

def delete_task_node(state):
    task_index = state.get("task_index")
    return {"response": delete_task(task_index)}

# Step 3: Create LangGraph Workflow
workflow = Graph()
workflow.add_node("add_task", add_task_node)
workflow.add_node("complete_task", complete_task_node)
workflow.add_node("list_tasks", list_tasks_node)
workflow.add_node("delete_task", delete_task_node)

# Define edges (simple linear flow for now)
workflow.add_edge("add_task", "list_tasks")
workflow.add_edge("complete_task", "list_tasks")
workflow.add_edge("delete_task", "list_tasks")

# Set entry point (default to list_tasks for simplicity)
workflow.set_entry_point("list_tasks")

# Compile the workflow
app = workflow.compile()

# Step 4: Create a Command-Line Interface
def main():
    while True:
        print("\n=== Task Manager ===")
        print("1. Add Task")
        print("2. Complete Task")
        print("3. List Tasks")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            task = input("Enter task: ")
            result = app.invoke({"task": task, "task_index": None})
            print(result["response"])
        elif choice == "2":
            task_index = int(input("Enter task index: "))
            result = app.invoke({"task_index": task_index, "task": None})
            print(result["response"])
        elif choice == "3":
            result = app.invoke({"task": None, "task_index": None})
            print(result["response"])
        elif choice == "4":
            task_index = int(input("Enter task index: "))
            result = app.invoke({"task_index": task_index, "task": None})
            print(result["response"])
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the CLI
if __name__ == "__main__":
    main()