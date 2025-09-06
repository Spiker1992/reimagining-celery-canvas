
from database import db, WorkflowLog
import json

def create_workflow(*tasks):
	"""
	Stores the list of tasks to be executed in the database.
	Each task is represented by its name and arguments.
	"""
	workflow_id = f"workflow_{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
	# Serialize tasks: store their names and args
	serialized_tasks = []
	for t in tasks:
		if hasattr(t, 'name'):
			serialized_tasks.append({'task': t.name, 'args': t.args, 'kwargs': t.kwargs})
		else:
			serialized_tasks.append(str(t))
	payload = json.dumps(serialized_tasks)
	log = WorkflowLog(workflow_id=workflow_id, payload=payload)
	db.add(log)
	db.commit()
	print(f"Workflow {workflow_id} created and tasks stored in DB.")
	return workflow_id