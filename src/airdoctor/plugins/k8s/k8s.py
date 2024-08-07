import json

import click
import yaml

from airdoctor.config import global_config
from airdoctor.tools import run_and_capture, write_output


@click.command("k8s")
@click.option("--namespace")
@click.option("--kubeconfig")
@click.option("--output-dir")
def cli(namespace, kubeconfig, output_dir):
    kubeconfig = kubeconfig or global_config.kubeconfig
    output_dir = output_dir or global_config.output_dir

    base_cmd = ["kubectl"]
    if kubeconfig:
        base_cmd.extend(["--kubeconfig", kubeconfig])

    cmd = []
    cmd.extend(base_cmd)
    cmd.extend(["get", "all,cm,secret,ing", "-o", "json"])
    if namespace:
        cmd.extend(["--namespace", namespace])
    else:
        cmd.extend(["-A"])

    res = run_and_capture(cmd)
    if res.returncode > 0:
        raise Exception("Failed to list k8s resources: " + res.stderr)

    data = yaml.safe_dump(json.loads(res.stdout))
    write_output(output_dir, "k8s", "all_resources", data)
