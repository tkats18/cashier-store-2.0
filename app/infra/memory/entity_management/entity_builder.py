from dataclasses import dataclass
from typing import Any, List, Optional, Protocol


@dataclass
class EntityField:
    field_name: str
    field_type: str


@dataclass
class Entity:
    name: str
    fields: List[EntityField]
    extra_values: List[str]

    def to_sql_representation(self) -> str:
        result = "CREATE TABLE " + self.name + " ("
        for i in self.fields:
            result += i.field_name + "   " + i.field_type + ", "
        result = result[0 : len(result) - 2] + " "

        if len(self.extra_values) == 0:
            return result + " );"

        for val in self.extra_values:
            result += val + ","

        result = result[0 : len(result) - 2] + " );"
        return result


class IEntityBuilder(Protocol):
    def with_field(self, name: str, value: Any) -> "IEntityBuilder":
        pass

    def with_extra_field(self, *, extra_field: str) -> "IEntityBuilder":
        pass

    def with_name(self, name: str) -> "IEntityBuilder":
        pass

    def build(self) -> Entity:
        pass


class EntityBuilder:
    def __init__(
        self,
        fields: Optional[List[EntityField]] = None,
        extra_fields: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.fields = fields or []
        self.extra_fields = extra_fields or []
        self.name = name or "unknown"

    def with_field(self, name: str, value: Any) -> "IEntityBuilder":
        self.fields.append(EntityField(name, value))

        return self

    def with_extra_field(self, *, extra_field: str) -> "IEntityBuilder":
        self.extra_fields.append(extra_field)
        return self

    def with_name(self, name: str) -> "IEntityBuilder":
        self.name = name
        return self

    def build(self) -> Entity:
        fields = []
        for i in self.fields:
            fields.append(EntityField(i.field_name, i.field_type))
        return Entity(self.name, fields, self.extra_fields)
