import click


@click.command("version")
@click.option("--domain")
def cli(domain):
    print("version" + domain)
