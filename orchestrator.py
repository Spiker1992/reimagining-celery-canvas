import json
import uuid
import time
from datetime import datetime
from celery import Celery, current_app

# --- Celery App Setup ---
# Assumes a Redis broker is running on localhost
app = Celery('custom_chain', broker='redis://localhost:6379/0')

# --- Dummy Database Functions ---
# These functions simulate the database interaction for storing and retrieving
# the workflow data. In a real-world scenario, you would replace these
# with your actual database queries (e.g., using SQLAlchemy, Django ORM, etc.)

def db_insert_workflow(workflow_id, serialized_tasks):
    """
    Simulates inserting the serialized workflow plan into the database.
    This would correspond to an INSERT statement into your `workflow_log` table.
    """
    print(f"--- Simulating Database Insertion ---")
    print(f"INSERT INTO workflow_log (workflow_id, timestamp, payload) VALUES ('{workflow_id}', '{datetime.utcnow().isoformat()}', '{serialized_tasks}')")
    print(f"-------------------------------------\n")
    # For this example, we'll store it in a simple dictionary in memory.
    # In a real app, this would be a database commit.
    app.current_task.request.kwargs['db_store'] = {
        'workflow_id': workflow_id,
        'payload': serialized_tasks
    }


def db_get_workflow(workflow_id):
    """
    Simulates retrieving the serialized workflow plan from the database.
    This would correspond to a SELECT statement from your `workflow_log` table.
    """
    print(f"--- Simulating Database Retrieval ---")
    print(f"SELECT payload FROM workflow_log WHERE workflow_id = '{workflow_id}' ORDER BY timestamp DESC LIMIT 1")
    print(f"-------------------------------------\n")
    # Retrieve from our in-memory store for this example
    if 'db_store' in app.current_task.request.kwargs:
        return app.current_task.request.kwargs['db_store']['payload']
    return None


# --- Custom Wrapper Function (Public API for your app) ---

def create_and_store_workflow(tasks_to_chain):
    """
    This is the public API function for your application. It takes a list
    of tasks, serializes them, stores the plan, and triggers the orchestrator.
    
    Args:
        tasks_to_chain (list): A list of dictionaries representing the tasks.
            Example: [{'task_name': 'tasks.task_a', 'args': [...]}]
    """
    # 1. Generate a unique workflow ID.
    workflow_id = str(uuid.uuid4())
    
    # 2. Serialize the task plan to a JSON string.
    serialized_plan = json.dumps(tasks_to_chain, indent=4)
    
    print(f"New workflow created with ID: {workflow_id}")
    print("Serialized task plan:")
    print(serialized_plan)
    
    # 3. Store the serialized plan in the database.
    db_insert_workflow(workflow_id, serialized_plan)
    
    # 4. Trigger the main orchestrator task with the workflow ID.
    orchestrator_task.delay(workflow_id)

# --- Example Usage ---
if __name__ == '__main__':
    print("--- Example 1: Running a successful workflow ---")
    tasks_to_run_1 = [
        {'task_name': 'custom_celery_chain.task_a', 'args': ['data from the start']},
        {'task_name': 'custom_celery_chain.task_b'},
        {'task_name': 'custom_celery_chain.task_c'}
    ]
    create_and_store_workflow(tasks_to_run_1)
    
    # Wait a bit to let the example run
    time.sleep(10)
    
    print("\n\n--- Example 2: Running a workflow that fails ---")
    tasks_to_run_2 = [
        {'task_name': 'custom_celery_chain.task_a', 'args': ['data from the start', {'error': True}]},
        {'task_name': 'custom_celery_chain.task_b'},
        {'task_name': 'custom_celery_chain.task_c'}
    ]
    create_and_store_workflow(tasks_to_run_2)
