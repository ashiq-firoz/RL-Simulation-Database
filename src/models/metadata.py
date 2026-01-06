from dataclasses import dataclass
from models.base import BaseModel

@dataclass
class Story(BaseModel):
    table_name = "stories"

    story_id: str
    task_id: str
    user_id: str
    text: str | None
    type: str
    created_at: str


@dataclass
class Tag(BaseModel):
    table_name = "tags"

    tag_id: str
    workspace_id: str
    name: str
    color: str | None
