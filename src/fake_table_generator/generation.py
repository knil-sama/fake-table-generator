import psycopg2 as pg
from faker import Faker
from enum import Enum, IntEnum
from typing import NamedTuple, List
import random
import re
import string
from tqdm import tqdm
from pathlib import Path


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


def to_pg_name(name: str):
    name_without_punctuation = re.sub("[" + string.punctuation + "]", "", name)
    return "_".join(name_without_punctuation.split()).lower()


class range_field:
    def __init__(self, fake, n):
        self.i = 0
        self.n = n
        self.fake = fake
        self.options_PostgresqlType = list(PostgresqlType)

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.n:
            self.i += 1
            random_name = to_pg_name(self.fake.name())
            return Field(random_name, random.choice(self.options_PostgresqlType))
        else:
            raise StopIteration()


def to_pg_schema(fake_table):
    sql = f"CREATE TABLE IF NOT EXISTS {fake_table.name} ( "
    sql += ", ".join(
        [f"{field.name} {field.type.value}" for field in fake_table.fields]
    )
    sql += ")"
    return sql


def generate_value(fake, field: PostgresqlType):
    value = "null"
    if field is PostgresqlType.text:
        valid_name = fake.name().replace("'", "")
        value = f"'{valid_name}'"
    elif field is PostgresqlType.timestamp:
        value = f"'{str(fake.date_time())}'"
    elif field is PostgresqlType.date:
        value = f"'{str(fake.date())}'"
    elif field is PostgresqlType.integer:
        value = str(random.randint(-5000, 5000))
    elif field is PostgresqlType.float:
        value = str(random.randint(-5000, 5000) * random.random())
    return value


def generate_rows_postgresql(fake, table: Table, nb_rows: int) -> str:
    values = ",".join(
        [
            f"({','.join([generate_value(fake,f.type) for f in table.fields])})"
            for _ in range(0, nb_rows)
        ]
    )
    return f"INSERT INTO {table.name} ({','.join([f.name for f in table.fields])}) VALUES {values}"


def generate_rows_csv(fake, table: Table, nb_rows: int) -> str:
    values = "\n".join(
        [
            f"{','.join([generate_value(fake,f.type) for f in table.fields])}"
            for _ in range(0, nb_rows)
        ]
    )
    return values


def main(
    target,
    nb_tables,
    nb_min_cols,
    nb_max_cols,
    nb_min_rows,
    nb_max_rows,
    available_types,
    languages: List[str],
):
    fake = Faker(languages)
    if target == TargetOutput.csv:
        for t in tqdm(range(nb_tables)):
            # define template data
            fake_fields = list(
                range_field(fake, random.randint(nb_min_cols, nb_max_cols + 1))
            )
            fake_table = Table(to_pg_name(fake.name()), fake_fields)
            with Path(f"{fake_table.name}.csv").open("w") as f:
                f.write(f"{','.join([f.name for f in fake_table.fields])}\n")
                rows = generate_rows_csv(
                    fake, fake_table, random.randint(nb_min_rows, nb_max_rows)
                )
                f.write(rows)


if __name__ == "__main__":
    fake = Faker(["it_IT", "en_US", "ja_JP", "he_IL", "zh_CN"])
    for t in range(1, 30):
        # define template data
        fake_fields = list(range_field(fake, random.randint(1, 50)))
        fake_table = Table(to_pg_name(fake.name()), fake_fields)
        conn = pg.connect(host="", database="", user="", password="")
        # use for test db so no need for transaction
        conn.set_session(autocommit=True)
        with conn.cursor() as cur:
            # create table
            cur.execute(to_pg_schema(fake_table))
            for i in tqdm(range(0, random.randint(1, 10000))):
                rows = generate_rows_postgresql(fake_table, 1000)
                cur.execute(rows)
        print(f"loaded table n{t}")
