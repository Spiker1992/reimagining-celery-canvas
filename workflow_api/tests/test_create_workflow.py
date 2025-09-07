import pytest
from workflow_api.tasks import task_a, task_b, task_c
from workflow_api.models import WorkflowLog
import json
import datetime

def create_workflow(*tasks):
    """
    Stores the list of tasks to be executed in the database.
    Each task is represented by its name and arguments.
    """
    workflow_id = f"workflow_{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
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

    print(f"Workflow {workflow_id} created and tasks stored in DB.")
    return workflow_id


@pytest.mark.django_db
def test_create_workflow_stores_tasks():
    workflow_id = create_workflow(
        task_a.s("data1"), task_b.s("data2"), task_c.s("data3")
    )
    # Fetch from DB
    log = WorkflowLog.objects.filter(workflow_id=workflow_id).first()
    assert log is not None
    tasks = json.loads(log.payload)
    assert len(tasks) == 3
    assert tasks[0]["task"] == "tasks.task_a"
    assert tasks[1]["task"] == "tasks.task_b"
    assert tasks[2]["task"] == "tasks.task_c"
