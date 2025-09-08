import pytest
from workflow_api.actions.create_workflow import create_workflow
from workflow_api.tasks import task_a, task_b, task_c
from workflow_api.models import WorkflowLog, WorkflowTask
import json
from django.db import IntegrityError


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
        {"task": "workflow_api.tasks.task_c", "args": ["data3"], "kwargs": {}},
    ]


@pytest.mark.django_db
def test_create_workflow_creates_execution_plan():
    workflow_id = create_workflow(
        task_a.s("data1"), task_b.s("data2"), task_c.s("data3")
    )

    tasks = WorkflowTask.objects.filter(workflow_id=workflow_id).order_by("sequence")

    assert tasks.count() == 3

    assert tasks[0].task_name == "workflow_api.tasks.task_a"
    assert tasks[0].args == ["data1"]
    assert tasks[0].kwargs == {}

    assert tasks[1].task_name == "workflow_api.tasks.task_b"
    assert tasks[1].args == ["data2"]
    assert tasks[1].kwargs == {}

    assert tasks[2].task_name == "workflow_api.tasks.task_c"
    assert tasks[2].args == ["data3"]
    assert tasks[2].kwargs == {}


@pytest.mark.django_db
def test_when_creating_empty_workflow_raise_exception():
    with pytest.raises(ValueError, match="At least one task must be provided to create a workflow."):
        create_workflow()


@pytest.mark.django_db
def test_create_workflow_rollback_on_failure(mocker):
    # Mock WorkflowTask.objects.create to raise an IntegrityError
    mocker.patch("workflow_api.models.WorkflowTask.objects.create", side_effect=IntegrityError)

    with pytest.raises(IntegrityError):
        create_workflow(
            task_a.s("data1"), task_b.s("data2"), task_c.s("data3")
        )

    # Ensure no WorkflowTask is created
    assert WorkflowTask.objects.count() == 0
    
    # Ensure no WorkflowLog is created
    assert WorkflowLog.objects.count() == 0
