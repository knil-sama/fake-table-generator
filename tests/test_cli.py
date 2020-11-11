from src.fake_table_generator import generate
import pytest


def test_generate_with_empty_parameters_raise_exception():
    with pytest.raises(SystemExit):
        generate()
