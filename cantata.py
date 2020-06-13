import stanza
import click
import lib.__init__ as init
import lib.stanza_utils as stanza_utils


version_num = ""

@click.group(invoke_without_command=True, no_args_is_help=True)
@click.option("-v", "--version", is_flag=True)
# === version ===
def cli(version):
    if version:
        click.echo("cantata version :"  + str(version_num))
        click.echo("By George Kowalski of MCW")


@cli.command()
@click.option("--dbfile", default="pyetl_fh.db")
def run_test_ner(dbfile):
    """
    Run a test of the software on self contained test data showing tokens and entities
    :param dbfile:
    :return:
    """
    stanza.download('en')  # download English model
    nlp = stanza.Pipeline('en', processors='tokenize,ner')  # initialize English neural pipeline
    doc = nlp(
        "\n\n  \nGeorge Kowalski works at the Medical College of WI.\n\n  \nChris Manning  works at Stanford University")  # run annotation over a sentence1
    # print ( doc)
    for sent in doc.sentences:
        print("------------ Sentence found ----------")
        print("Tokens")
        for token in sent.tokens:
            print(f'\ttoken: {token.text}\tner: {token.ner}\t start {token.start_char}\tend {token.end_char}')
        print("Entities")
        for token in sent.ents:
            print(f'\tentity: {token.text}\tner: {token.type}\t start {token.start_char}\tend {token.end_char}')


if __name__ == "__main__":
    version_num = str(init.__VERSION__)
    cli()
