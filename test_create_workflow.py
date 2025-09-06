import pytest
from main import create_workflow
from tasks import task_a, task_b, task_c
from database import db, WorkflowLog
import json

@pytest.fixture(autouse=True)
def clean_db():
    db.query(WorkflowLog).delete()
    db.commit()

def test_create_workflow_stores_tasks():
    workflow_id = create_workflow(
        task_a.s("data1"),
        task_b.s("data2"),
        task_c.s("data3")
    )
    # Fetch from DB
    log = db.query(WorkflowLog).filter_by(workflow_id=workflow_id).first()
    assert log is not None
    tasks = json.loads(log.payload)
    assert len(tasks) == 3
    assert tasks[0]['task'] == 'tasks.task_a'
    assert tasks[1]['task'] == 'tasks.task_b'
    assert tasks[2]['task'] == 'tasks.task_c'
