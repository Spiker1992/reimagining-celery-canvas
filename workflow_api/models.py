from django.db import models

# Create your models here.

class WorkflowLog(models.Model):
    workflow_id = models.CharField(max_length=255, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField()

    def __str__(self):
        return f"WorkflowLog({self.workflow_id})"
