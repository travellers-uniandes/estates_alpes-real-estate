from dataclasses import dataclass, field
from app.seedwork.aplication.dto import DTO


@dataclass(frozen=True)
class ListDTO(DTO):
    code: str = field(default_factory=str)
    name: str = field(default_factory=str)
    id: str = field(default_factory=str)
