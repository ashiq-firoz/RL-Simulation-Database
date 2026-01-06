from dataclasses import dataclass
from models.base import BaseModel

@dataclass
class Task(BaseModel):
    table_name = "tasks"

    task_id: str
    project_id: str | None
    section_id: str | None
    parent_task_id: str | None
    assignee_id: str | None
    creator_id: str
    name: str
    description: str | None
    priority: str | None
    due_date: str | None
    start_date: str | None
    completed: bool = False
    completed_at: str | None = None
    created_at: str = ""
    updated_at: str = ""
