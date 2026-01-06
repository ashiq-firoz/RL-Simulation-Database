from dataclasses import dataclass
from models.base import BaseModel

@dataclass
class Workspace(BaseModel):
    table_name = "workspaces"

    workspace_id: str
    name: str
    domain: str | None
    created_at: str | None = None
