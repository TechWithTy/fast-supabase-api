from pydantic import BaseModel, Field
from datetime import datetime

class TaskDelete(BaseModel):
    """Called whenever a task is deleted"""
    type: str = Field(..., description="Event type")
    locationId: str = Field(..., description="Location ID")
    id: str = Field(..., description="Task ID")
    assignedTo: str = Field(..., description="Assigned user ID")
    body: str = Field(..., description="Task body")
    contactId: str = Field(..., description="Associated contact ID")
    title: str = Field(..., description="Task title")
    dateAdded: datetime = Field(..., description="Date the task was added")
    dueDate: datetime = Field(..., description="Due date of the task")

# Example usage:
example_data = {
    "type": "TaskDelete",
    "locationId": "ve9EPM428h8vShlRW1KT",
    "id": "UlRWGLSXh0ji5qbiGu4i",
    "assignedTo": "63e4qiWDsFJjOYAC8phG",
    "body": "Loram ipsum",
    "contactId": "CWBf1PR9LvvBkcYqiXlc",
    "title": "Loram ipsum",
    "dateAdded": "2021-11-26T12:41:02.193Z",
    "dueDate": "2021-11-26T12:41:02.193Z"
}

task_delete = TaskDelete(**example_data)
print(task_delete)