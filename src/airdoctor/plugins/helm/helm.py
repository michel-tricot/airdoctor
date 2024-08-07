import itertools
import json
import random
import string

import click

from airdoctor.config import global_config
from airdoctor.tools import run_and_capture, write_output

DEFAULT_CHART_KEYWORDS = ["nginx", "airbyte"]


@click.command("helm")
@click.argument("chart-keywords", nargs=-1)
@click.option("--namespace")
@click.option("--kubeconfig")
@click.option("--output-dir")
def cli(chart_keywords, namespace, kubeconfig, output_dir):
    kubeconfig = kubeconfig or global_config.kubeconfig
    chart_keywords = chart_keywords or DEFAULT_CHART_KEYWORDS
    output_dir = output_dir or global_config.output_dir

    base_cmd = ["helm"]
    if kubeconfig:
        base_cmd.extend(["--kubeconfig", kubeconfig])

    charts = list_charts(base_cmd, namespace)
    charts = [chart for chart in charts if any(pattern in chart["chart"] for pattern in chart_keywords)]

    # weird hack because helm doesn't spit out configs for the namespace associated with the chart
    namespaces = (chart["namespace"] for chart in charts)
    categories = ["hooks", "manifest", "metadata", "notes", "values"]
    for chart, chart_namespace, category in itertools.product(charts, namespaces, categories):
        yaml_configs = retrieve_yaml_configs(base_cmd, category, chart["name"], chart_namespace)
        for y in yaml_configs:
            if y.startswith("# Source: "):
                filename = y.split("\n", 1)[0].replace("# Source: ", "").replace("/", "_")
            else:
                filename = "".join(random.choices(string.ascii_uppercase + string.digits, k=7))

            write_output(output_dir, "helm", filename, y, category)


def list_charts(base_cmd, namespace):
    cmd = []
    cmd.extend(base_cmd)
    cmd.extend(["list", "-o", "json"])
    if namespace:
        cmd.extend(["--namespace", namespace])
    else:
        cmd.extend(["-A"])
    res = run_and_capture(cmd)
    if res.returncode > 0:
        raise Exception("Failed to list charts: " + res.stderr)

    return json.loads(res.stdout)


def retrieve_yaml_configs(base_cmd, category, chart_name, chart_namespace):
    cmd = []
    cmd.extend(base_cmd)
    cmd.extend(["get", category, chart_name, "-n", chart_namespace])

    res = run_and_capture(cmd)
    if res.returncode > 0:
        return []

    results = []
    current_file = None
    for line in res.stdout.split("\n"):
        if not current_file:
            current_file = []
            results.append(current_file)

        if line == "---":
            current_file = None
        else:
            current_file.append(line)

    return ["\n".join(current_file) for current_file in results]
