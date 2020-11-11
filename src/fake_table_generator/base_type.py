from typing import NamedTuple, List
from enum import IntEnum, Enum
import random
import re
import string


class TargetOutput(IntEnum):
    postgresql = 1
    csv = 2


class PostgresqlType(Enum):
    date = "date"
    timestamp = "timestamp"
    integer = "integer"
    float = "float"
    text = "text"
    # TODO jsonb


class Field(NamedTuple):
    name: str
    type: PostgresqlType


class Table(NamedTuple):
    name: str
    fields: List[Field]


class RangeFieldsGenerator:
    def __init__(self, fake, max_number_fields: int):
        self.i = 0
        self.max_number_fields = max_number_fields
        self.fake = fake
        self.options_PostgresqlType = list(PostgresqlType)

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.max_number_fields:
            self.i += 1
            random_name = to_pg_name(self.fake.name())
            return Field(random_name, random.choice(self.options_PostgresqlType))
        else:
            raise StopIteration()


def to_pg_name(name: str) -> str:
    name_without_punctuation = re.sub("[" + string.punctuation + "]", "", name)
    return "_".join(name_without_punctuation.split()).lower()
