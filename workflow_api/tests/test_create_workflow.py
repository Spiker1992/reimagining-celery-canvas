import pytest
from workflow_api.actions.create_workflow import create_workflow
from workflow_api.tasks import task_a, task_b, task_c
from workflow_api.models import WorkflowLog
import json


@pytest.mark.django_db
def test_create_workflow_stores_tasks():
    workflow_id = create_workflow(
        task_a.s("data1"), task_b.s("data2"), task_c.s("data3")
    )

    log = WorkflowLog.objects.filter(workflow_id=workflow_id).first()

    assert log is not None

    tasks = json.loads(log.payload)
    
    assert tasks == [
        {"task": "workflow_api.tasks.task_a", "args": ["data1"], "kwargs": {}},
        {"task": "workflow_api.tasks.task_b", "args": ["data2"], "kwargs": {}}, 
        {"task": "workflow_api.tasks.task_c", "args": ["data3"], "kwargs": {}}
    ]

@pytest.mark.django_db
def test_when_creating_empty_workflow_raise_exception():
    with pytest.raises(ValueError, match="At least one task must be provided to create a workflow."):
        create_workflow()