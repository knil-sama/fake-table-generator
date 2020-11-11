from src.fake_table_generator.generation import to_pg_schema, generate_value
from src.fake_table_generator.base_type import Table, Field, PostgresqlType
from faker import Faker
import datetime


def test_to_pg_schema():
    fake_table = Table(
        "test",
        [Field("id", PostgresqlType.integer), Field("cols2", PostgresqlType.date)],
    )
    expected_schema = """CREATE TABLE IF NOT EXISTS test (
id integer
, cols2 date
);"""
    assert expected_schema == to_pg_schema(fake_table)


def test_generate_value_default():
    assert "null" == generate_value(None, None)


def test_generate_value():
    fake = Faker()
    assert len(generate_value(fake, PostgresqlType.text)) > 0
    int(generate_value(fake, PostgresqlType.integer))
    float(generate_value(fake, PostgresqlType.float))
    datetime.datetime.strptime(
        generate_value(fake, PostgresqlType.timestamp), "'%Y-%m-%d %H:%M:%S'"
    )
    datetime.datetime.strptime(generate_value(fake, PostgresqlType.date), "'%Y-%m-%d'")
