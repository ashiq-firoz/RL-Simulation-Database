from dataclasses import dataclass
from models.base import BaseModel

@dataclass
class Project(BaseModel):
    table_name = "projects"

    project_id: str
    team_id: str
    owner_id: str | None
    name: str
    description: str | None
    status: str | None
    due_date: str | None
    created_at: str
    archived: bool = False
