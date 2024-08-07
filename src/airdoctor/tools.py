import logging
import os
import subprocess


def run_and_capture(cmd):
    logging.debug("Running command: %s", cmd)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        logging.warning(f"Failed command: {cmd} ({res.stderr.strip()})")
    return res


def write_output(base_dir, plugin_name, filename, data, subdir=None):
    dst = os.path.join(base_dir, plugin_name or "", subdir or "", filename)
    if os.path.exists(dst):
        logging.warning(f"Clobbering output file: {dst}")

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w") as f:
        f.write(data)
