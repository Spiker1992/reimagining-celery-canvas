from django.db import models

# Create your models here.

PENDING = "pending"
IN_PROGRESS = "in_progress"
COMPLETED = "completed"
FAILED = "failed"

WORKFLOW_STATUSES = [
    (PENDING, "Pending"),
    (IN_PROGRESS, "In Progress"),
    (COMPLETED, "Completed"),
    (FAILED, "Failed"),
]

class WorkflowLog(models.Model):
    workflow_id = models.CharField(max_length=255, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    status = models.CharField(max_length=50, choices=WORKFLOW_STATUSES, default=PENDING)

    def __str__(self):
        return f"WorkflowLog({self.workflow_id})"

class WorkflowTask(models.Model):
    workflow_id = models.CharField(max_length=255, db_index=True)
    task_name = models.TextField()
    args = models.JSONField()
    kwargs = models.JSONField()
    sequence = models.IntegerField()

    def __str__(self):
        return f"WorkflowTask({self.workflow_id}, {self.task_name}, {self.sequence})"
