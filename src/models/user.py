from dataclasses import dataclass
from models.base import BaseModel

@dataclass
class User(BaseModel):
    table_name = "users"

    user_id: str
    workspace_id: str
    email: str
    full_name: str
    job_title: str | None
    avatar_url: str | None
    created_at: str
