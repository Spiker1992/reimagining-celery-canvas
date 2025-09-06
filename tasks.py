from celery import app

@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def task_a(self, data):
    """A dummy task that processes some data."""
    print(f"Executing Task A: {data}")
    # Simulate a transient failure to test retry logic
    if 'error' in data:
        raise ValueError("Task A failed due to an intentional error.")
    time.sleep(1)
    result = f"Processed by Task A: {data}"
    return result

@app.task(bind=True)
def task_b(self, data):
    """A dummy task that processes data from the previous task."""
    print(f"Executing Task B with data from previous task: {data}")
    time.sleep(1)
    result = f"Processed by Task B: {data}"
    return result

@app.task(bind=True)
def task_c(self, data):
    """A final task that saves the result."""
    print(f"Executing Task C with data from previous task: {data}")
    time.sleep(1)
    result = f"Final result: {data}"
    return result

