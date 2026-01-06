from dataclasses import asdict
from typing import Type, TypeVar, List
from utils.db import get_db_connection

T = TypeVar("T")

class BaseModel:
    table_name: str

    @classmethod
    def from_row(cls: Type[T], row) -> T:
        return cls(**dict(row))

    @classmethod
    def get_by_id(cls: Type[T], pk_name: str, pk_value: str) -> T | None:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"SELECT * FROM {cls.table_name} WHERE {pk_name} = ?"
        cursor.execute(query, (pk_value,))
        row = cursor.fetchone()
        conn.close()

        return cls.from_row(row) if row else None

    def insert(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        data = asdict(self)
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))

        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        conn.close()
