from typing import Any, List
from workflow_api.actions.execute_workflow_task import execute_workflow_task
from workflow_api.models import WorkflowLog, WorkflowTask
import json
from uuid import uuid4
from django.db import transaction
import logging
from celery import signals

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
def create_workflow(workflow_name: str, *tasks: Any) -> uuid4:
    """
    Stores the workflow name and list of tasks to be executed in the database.
    Each task is represented by its name and arguments.
    """
    if not tasks:
        raise ValueError("At least one task must be provided to create a workflow.")

    workflow_id = uuid4()

    # Save workflow name in WorkflowLog
    WorkflowLog.objects.create(workflow_id=workflow_id, name=workflow_name)

    save_workflow_tasks(workflow_id, tasks)
    
    execute_workflow_task(workflow_id)

    logger.info(f"Workflow {workflow_id} with name '{workflow_name}' created and tasks stored in DB.")
    return workflow_id

@signals.task_postrun.connect
def task_status_update(sender=None, task_id=None, task=None, args=None, kwargs=None, retval=None, state=None, **other):
    """Signal handler to update the workflow log status after a task is run."""
    if not hasattr(task, "workflow_id"):
        return

    workflow_id = task.workflow_id
    try:
        log = WorkflowLog.objects.get(workflow_id=workflow_id)
        if state == "SUCCESS":
            log.status = "completed"
        elif state == "FAILURE":
            log.status = "failed"
        else:
            log.status = "in_progress"
        log.save()
        logger.info(f"Workflow {workflow_id} status updated to {log.status}.")
    except WorkflowLog.DoesNotExist:
        logger.error(f"WorkflowLog with ID {workflow_id} does not exist.")