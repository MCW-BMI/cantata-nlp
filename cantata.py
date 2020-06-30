import click
import lib.__init__ as init
import lib.stanza_utils as stanza_utils
# Copyright
from lib import spacy_utils

version_num = ""

@click.group(invoke_without_command=True, no_args_is_help=True)
@click.option("-v", "--version", is_flag=True)
# === version ===
def cli(version):
    if version:
        click.echo("cantata version :"  + str(version_num))
        click.echo("By George Kowalski of MCW")


@cli.command()
@click.option("--lib", default="spacy")
def run_test_ner(lib):
    """
    Run a test of the software on self contained test data showing tokens and entities
    :param dbfile:
    :return:
    """
    if lib == 'spacy':
        spacy_utils.run_test_ner()
    else:
        stanza_utils.run_test_ner()

@cli.command()
@click.argument("input_dir", nargs=1)
@click.argument("output_dir", nargs=1)
@click.option("--file")
@click.option("--lib", default="spacy")
def run_ner_cd2h(input_dir, output_dir, lib, file):
    """
    Run a test of the software on self contained test data showing tokens and entities
    :param dbfile:
    :return:
    """
    if lib == "spacy":
        spacy_utils.run_cd2h(input_dir, output_dir, file)
    else:
        stanza_utils.run_ner_cd2h(input_dir, output_dir)


if __name__ == "__main__":
    version_num = str(init.__VERSION__)
    cli()
