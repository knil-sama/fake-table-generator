from src.fake_table_generator.base_type import to_pg_name


def test_to_pg_name():
    assert "valid_name" == to_pg_name("val.@^!id %Name")
