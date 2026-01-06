from dataclasses import dataclass
from models.base import BaseModel

@dataclass
class CustomFieldDefinition(BaseModel):
    table_name = "custom_field_definitions"

    field_id: str
    workspace_id: str
    name: str
    type: str
    description: str | None


@dataclass
class CustomFieldOption(BaseModel):
    table_name = "custom_field_options"

    option_id: str
    field_id: str
    value: str
    color: str | None
    order_index: int | None


@dataclass
class CustomFieldValue(BaseModel):
    table_name = "custom_field_values"

    value_id: str
    task_id: str
    field_id: str
    value_text: str | None
    value_number: float | None
    value_date: str | None
    value_enum_option_id: str | None
