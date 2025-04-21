from pydantic import BaseModel, Field
from datetime import datetime

class TaskCreate(BaseModel):
    type: str = Field(..., description="Type of the webhook event")
    locationId: str = Field(..., description="Unique identifier for the location")
    id: str = Field(..., description="Unique identifier for the task")
    assignedTo: str = Field(..., description="User ID the task is assigned to")
    body: str = Field(..., description="Content of the task")
    contactId: str = Field(..., description="Unique identifier for the associated contact")
    title: str = Field(..., description="Title of the task")
    dateAdded: datetime = Field(..., description="Date and time when the task was added")
    dueDate: datetime = Field(..., description="Due date and time for the task")

    class Config:
        allow_population_by_field_name = True

# Example usage
example_data = {
    "type": "TaskCreate",
    "locationId": "ve9EPM428h8vShlRW1KT",
    "id": "UlRWGLSXh0ji5qbiGu4i",
    "assignedTo": "63e4qiWDsFJjOYAC8phG",
    "body": "Loram ipsum",
    "contactId": "CWBf1PR9LvvBkcYqiXlc",
    "title": "Loram ipsum",
    "dateAdded": "2021-11-26T12:41:02.193Z",
    "dueDate": "2021-11-26T12:41:02.193Z"
}

task_create = TaskCreate(**example_data)
print(task_create)