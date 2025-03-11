from dataclasses import dataclass
from uuid import UUID


@dataclass
class User:
    user_id: UUID
    first_name: str
    last_name: str
    patronymic: str
    email: str
    hashed_password: str
    is_admin: bool = False
