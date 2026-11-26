"""Conda route helpers for benchmark.yaml.

  sync         copy each environment's conda export from its module repository,
               at the commit benchmark.yaml pins, to the environment's `conda:` path
  check        like sync, but only report copies that differ (exit 1 if any)
  conda-plan   write benchmark.conda.yaml: benchmark.yaml with the conda backend

Each environment's source path is in envs/sources.yaml; its repository and
commit come from the modules in benchmark.yaml that use it. --from-dir DIR
reads <DIR>/<repo name>/<path> from local working trees instead (development).
"""

import argparse
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT / "benchmark.yaml"
CONDA_PLAN = ROOT / "benchmark.conda.yaml"


def env_sources(plan):
    """env id -> (repository url, commit), from the modules using the env."""
    found = {}
    for stage in plan["stages"]:
        for module in stage.get("modules", []):
            env = module.get("software_environment")
            repo = module["repository"]
            ref = (repo["url"], str(repo["commit"]))
            if env in found and found[env] != ref:
                sys.exit(f"{env}: modules pin different repositories/commits: {found[env]} vs {ref}")
            found[env] = ref
    return found


def fetch(url, commit, path, from_dir):
    name = url.rstrip("/").removesuffix(".git").rsplit("/", 1)[-1]
    if from_dir:
        return (Path(from_dir) / name / path).read_text()
    if url.startswith("/"):
        return subprocess.run(["git", "-C", url, "show", f"{commit}:{path}"],
                              check=True, capture_output=True, text=True).stdout
    m = re.match(r"https://github\.com/([^/]+/[^/]+?)(?:\.git)?$", url)
    if not m:
        sys.exit(f"don't know how to fetch from {url}")
    raw = f"https://raw.githubusercontent.com/{m.group(1)}/{commit}/{path}"
    with urllib.request.urlopen(raw) as r:
        return r.read().decode()


def sync(check, from_dir):
    plan = yaml.safe_load(PLAN.read_text())
    sources = yaml.safe_load((ROOT / "envs" / "sources.yaml").read_text())
    refs = env_sources(plan)
    stale = []
    for env_id, env in plan["software_environments"].items():
        if "conda" not in env:
            continue
        if env_id not in sources:
            sys.exit(f"{env_id}: no source path in envs/sources.yaml")
        if env_id not in refs:
            print(f"{env_id}: no module uses it, skipped")
            continue
        url, commit = refs[env_id]
        text = fetch(url, commit, sources[env_id], from_dir)
        dest = ROOT / env["conda"]
        current = dest.read_text() if dest.exists() else None
        if current == text:
            continue
        stale.append(env_id)
        if check:
            print(f"{env_id}: {env['conda']} differs from {url}@{commit}:{sources[env_id]}")
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(text)
            print(f"{env_id}: {env['conda']} <- {url}@{commit}:{sources[env_id]}")
    if check and stale:
        sys.exit(1)


def conda_plan():
    text = PLAN.read_text()
    new, n = re.subn(r"(?m)^software_backend: \S+$", "software_backend: conda", text)
    if n != 1:
        sys.exit("benchmark.yaml: expected exactly one top-level software_backend line")
    CONDA_PLAN.write_text("# generated from benchmark.yaml by `pixi run conda-plan`; do not edit\n" + new)
    print(f"wrote {CONDA_PLAN.name}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command", choices=["sync", "check", "conda-plan"])
    p.add_argument("--from-dir", help="read exports from local repository checkouts under DIR")
    a = p.parse_args()
    if a.command == "conda-plan":
        conda_plan()
    else:
        sync(a.command == "check", a.from_dir)


if __name__ == "__main__":
    main()
