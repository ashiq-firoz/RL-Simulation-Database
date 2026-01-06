from dataclasses import dataclass
from models.base import BaseModel

@dataclass
class Team(BaseModel):
    table_name = "teams"

    team_id: str
    workspace_id: str
    name: str
    description: str | None
    created_at: str
