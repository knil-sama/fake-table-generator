import psycopg2 as pg
from faker import Faker
from enum import Enum, IntEnum
from typing import NamedTuple, List
import random
from tqdm import tqdm
from pathlib import Path
from .base_type import (
    PostgresqlType,
    Table,
    TargetOutput,
    RangeFieldsGenerator,
    to_pg_name,
)
import logging

logger = logging.getLogger(__name__)


def to_pg_schema(fake_table: Table) -> str:
    sql = f"CREATE TABLE IF NOT EXISTS {fake_table.name} (\n"
    sql += ", ".join(
        [f"{field.name} {field.type.value}\n" for field in fake_table.fields]
    )
    sql += ");"
    return sql


def generate_value(fake, field: PostgresqlType) -> str:
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
    logging.infos(
        f"generated {nb_rows} for table {table.name} with fields {[field for field in table.fields]}"
    )
    return values


def generate(
    target: TargetOutput,
    nb_tables: int,
    nb_min_cols: int,
    nb_max_cols: int,
    nb_min_rows: int,
    nb_max_rows: int,
    available_types: List[PostgresqlType],
    languages: List[str],
) -> None:
    fake = Faker(languages)
    if target == TargetOutput.csv:
        for t in tqdm(range(nb_tables)):
            # define template data
            fake_fields = list(
                RangeFieldsGenerator(fake, random.randint(nb_min_cols, nb_max_cols + 1))
            )
            fake_table = Table(to_pg_name(fake.name()), fake_fields)
            with Path(f"{fake_table.name}.csv").open("w") as f:
                f.write(f"{','.join([f.name for f in fake_table.fields])}\n")
                rows = generate_rows_csv(
                    fake, fake_table, random.randint(nb_min_rows, nb_max_rows)
                )
                f.write(rows)
