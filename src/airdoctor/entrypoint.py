"""Command line interface for Airdoctor."""

import importlib
import logging
import os
import pkgutil

import click
import coloredlogs
import dotenv

import airdoctor.plugins
from airdoctor.config import global_config

field_styles = dict(coloredlogs.DEFAULT_FIELD_STYLES)
field_styles["levelname"] = {"color": "white"}
coloredlogs.install(fmt="%(asctime)s %(levelname)s %(message)s", field_styles=field_styles)

DEFAULT_ABCTL_KUBECONFIG_PATH = os.path.expanduser("~/.airbyte/abctl/abctl.kubeconfig")


@click.group()
@click.version_option()
@click.option("-d", "--debug", is_flag=True, show_envvar=True, envvar="DEBUG", help="Enable debug logs")
@click.option("--output-dir", help="Directory collecting all diagnosis information")
@click.option("--kubeconfig", show_envvar=True, envvar="KUBECONFIG", help="Path to kubeconfig file")
@click.option("--access-token", show_envvar=True, envvar="ACCESS_TOKEN", help="Token to access Airbyte's API")
@click.option("--local", is_flag=True, help="Assume abctl local deploy")
def cli(debug, output_dir, local, kubeconfig, access_token):
    """CLI to audit your Airbyte install."""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Debug flag activated")

    if local:
        if not kubeconfig and os.path.isfile(DEFAULT_ABCTL_KUBECONFIG_PATH):
            kubeconfig = DEFAULT_ABCTL_KUBECONFIG_PATH

    global_config.kubeconfig = kubeconfig
    global_config.access_token = access_token
    global_config.output_dir = output_dir

    logging.debug(global_config)


@cli.group(name="run")
def run():
    """Select a diagnosis to run"""


# Register all existing plugins
for module in pkgutil.iter_modules(airdoctor.plugins.__path__):
    m = importlib.import_module(f"airdoctor.plugins.{module.name}")
    run.add_command(m.cli)


@cli.command()
def diagnose():
    """Run the all diagnosis"""


def main():
    try:
        dotenv.load_dotenv()
        cli()
    except Exception as e:
        click.echo(e)
        return 1
