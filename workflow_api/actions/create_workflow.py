from workflow_api.models import WorkflowLog, WorkflowTask
import json
from uuid import uuid4
from django.db import transaction

@transaction.atomic
def create_workflow(*tasks):
    """
    Stores the list of tasks to be executed in the database.
    Each task is represented by its name and arguments.
    """
    if not tasks:
        raise ValueError("At least one task must be provided to create a workflow.")

    workflow_id = uuid4()
    # Serialize tasks: store their names and args
    serialized_tasks = []
    for t in tasks:
        if hasattr(t, "name"):
            serialized_tasks.append(
                {"task": t.name, "args": t.args, "kwargs": t.kwargs}
            )
        else:
            serialized_tasks.append(str(t))
    payload = json.dumps(serialized_tasks)

    log = WorkflowLog(workflow_id=workflow_id, payload=payload)
    log.save()
    print(f"Workflow {workflow_id} created and tasks stored in DB.")

    for sequence, t in enumerate(tasks):
        if hasattr(t, "name"):
            WorkflowTask.objects.create(
                workflow_id=workflow_id,
                task_name=t.name,
                args=t.args,
                kwargs=t.kwargs,
                sequence=sequence
            )

    return workflow_id
