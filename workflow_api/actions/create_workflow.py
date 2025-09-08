from typing import Any, List
from workflow_api.models import WorkflowLog, WorkflowTask
import json
from uuid import uuid4
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

def serialize_task(task: Any) -> dict:
    """Serialize a task into a dictionary."""
    if hasattr(task, "name"):
        return {"task": task.name, "args": task.args, "kwargs": task.kwargs}
    return {"task": str(task)}

def save_workflow_log(workflow_id: uuid4, serialized_tasks: List[dict]) -> None:
    """Save the workflow log to the database."""
    payload = json.dumps(serialized_tasks)
    WorkflowLog.objects.create(workflow_id=workflow_id, payload=payload)

def save_workflow_tasks(workflow_id: uuid4, tasks: List[Any]) -> None:
    """Save individual workflow tasks to the database."""
    for sequence, task in enumerate(tasks):
        if hasattr(task, "name"):
            WorkflowTask.objects.create(
                workflow_id=workflow_id,
                task_name=task.name,
                args=task.args,
                kwargs=task.kwargs,
                sequence=sequence
            )

@transaction.atomic
def create_workflow(*tasks: Any) -> uuid4:
    """
    Stores the list of tasks to be executed in the database.
    Each task is represented by its name and arguments.
    """
    if not tasks:
        raise ValueError("At least one task must be provided to create a workflow.")

    workflow_id = uuid4()
    serialized_tasks = [serialize_task(task) for task in tasks]

    save_workflow_log(workflow_id, serialized_tasks)
    save_workflow_tasks(workflow_id, tasks)

    logger.info(f"Workflow {workflow_id} created and tasks stored in DB.")
    return workflow_id