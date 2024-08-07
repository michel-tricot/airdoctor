import click


@click.command("logs")
@click.option("--domain")
def cli(domain):
    print("logs " + domain)
