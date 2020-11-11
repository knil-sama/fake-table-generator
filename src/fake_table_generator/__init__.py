from .generation import TargetOutput, PostgresqlType, main
from typing import List
import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--target', type=click.Choice([el.name for el in TargetOutput]), default = TargetOutput.csv.name)
@click.option('--nb_tables', type=click.IntRange(min=1), required=True)
@click.option('--nb_min_cols', type=int, default=1)
@click.option('--nb_max_cols', type=int, default=1)
@click.option('--nb_min_rows', type=int, default=50)
@click.option('--nb_max_rows', type=int, default=100)
@click.option('--available_types', type=click.Choice([el.name for el in PostgresqlType]), multiple=True, default=[el.name for el in PostgresqlType])
@click.option('--languages', type=str, multiple=True, default= ['en_US'])
def generate(target, nb_tables, nb_min_cols, nb_max_cols, nb_min_rows, nb_max_rows, available_types, languages):
    main(TargetOutput[target], nb_tables, nb_min_cols, nb_max_cols, nb_min_rows, nb_max_rows, [PostgresqlType(el) for el in available_types], languages)

cli.add_command(generate)

if __name__ == "__main__":
    cli()
