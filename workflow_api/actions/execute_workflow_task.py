
from workflow_api.models import WorkflowTask
from workflow_project.celery import app

def execute_workflow_task(workflow_id):
    """Execute the first task in the workflow."""
    first_task = WorkflowTask.objects.filter(workflow_id=workflow_id).order_by("sequence").first()
    
    if not first_task:
        raise ValueError("No tasks found for the given workflow ID.")

    # Simulate task execution (replace with actual task execution logic)
    task_name = first_task.task_name
    args = first_task.args
    kwargs = first_task.kwargs

    task_func = app.tasks[task_name]
    task_func.delay_on_commit(workflow_id, *args, **kwargs)
    # Log the execution (for now, just print)
    print(f"Executing task: {task_name} with args: {args} and kwargs: {kwargs}")

    return task_name, args, kwargs
