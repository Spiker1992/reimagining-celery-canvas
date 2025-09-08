# reimagining-celery-canvas

# Why 

Celery canvas has some issues when it comes to being reliable. 
Celery backend doesn't support tracking canvas workflows.

## Example
- A step fails in a workflow: step and all remaining tasks are marked as failed. There is no clear link between all items in the workflow.
- System goes down (while late acks are false): Celery backend will record those as `STARTED` or `PENDING`. Any children will be in a limbo - there is no clear link between all items in the workflow.

### Impact
- You dont know which tasks belong to which workflow
- You cant simply restart tasks

This becomes especially problematic when you run hundreds of thousands tasks. Even a short lasting issue can result in a lot of orphaned tasks.

# Plan
## Capture execution plan
We first create a workflow and capture the plan. 

This should be an atomic action. If any failures happen workflow wouldn't be created.

## Create execution plan

Once we have a workflow, we need to create a list of tasks to be executed.

Each task will be executed one at a time.

## Execution

Items from the execution list will be processed in order
by calling the respective task with its args and kwargs

for each task we track its status (pending, running, completed, failed)
and the result or error message if applicable

- tasks would be triggered right away
- using signals we should be able to manage tasks progress
- once we get a signal of success, task will be moved to the next one

## Completion

once all tasks are completed, we mark the workflow as completed

# Install 
- pip install -r requirements.txt 
- docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
- docker stop rabbitmq
- docker rm rabbitmq