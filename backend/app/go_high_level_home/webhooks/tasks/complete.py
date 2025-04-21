from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskComplete(BaseModel):
    type: str = Field(..., description="Type of the webhook event")
    locationId: str = Field(..., description="Unique identifier for the location")
    id: str = Field(..., description="Unique identifier for the task")
    assignedTo: str = Field(..., description="User ID the task is assigned to")
    body: str = Field(..., description="Content of the task")
    contactId: str = Field(..., description="Associated contact ID")
    title: str = Field(..., description="Title of the task")
    dateAdded: datetime = Field(..., description="Date and time when the task was added")
    dueDate: datetime = Field(..., description="Due date and time of the task")

    class Config:
        allow_population_by_field_name = True

# Example usage
example_data = {
    "type": "TaskComplete",
    "locationId": "ve9EPM428h8vShlRW1KT",
    "id": "5HrB1IbmnKMBXloldFuP",
    "assignedTo": "bNl8QNGXhIQJLv8eeASQ",
    "body": "testing",
    "contactId": "WFwVrSSjZ2CNHbZThQX2",
    "dateAdded": "2021-11-29T13:37:28.304Z",
    "dueDate": "2021-12-22T06:55:00.000Z",
    "title": "test"
}

task_complete = TaskComplete(**example_data)
print(task_complete)