# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Upcoming

### Changed

- port to omnibenchmark api 0.8: named entrypoints (one module per dataset and per pipeline), underscore ids, `--output id=PATH` outputs
- modules own their environments (pixi/rv lock projects built into GHCR images); the plan's apptainer definitions are gone
- `metrics` is a gather per dataset (tidy `metrics.tsv`, one row per run and clustering algorithm); the report is a global gather instead of a metric collector
- phase timings are obkit events (`obkit-events.jsonl`) instead of `timings.json`
- omnibenchmark is pinned in `pixi.toml`; CI validates with it

### Added

- conda route: every environment also has a pinned conda file synced from its module (`pixi run sync-envs`, `pixi run run-conda`)
- brisc and bixverse pipelines (ported by Mark Robinson in omni-training)

## [v1.1](https://github.com/scrna-bench/pipelines-plan/releases/tag/v1.1)

### Added

- reparameterize `n_cluster` (number of clusters) with `d_cluster` (delta number of clusters with respect to true number of clusters for a dataset)
- average leiden and louvain times across multiple function calls
- add GPU load times for the `rapids` pipeline

## [v1.0](https://github.com/scrna-bench/pipelines-plan/releases/tag/v1.0)

A benchmark of single-cell RNAseq analysis pipelines focused on preprocessing.

The repo includes a benchmark plan that can be used in isolation to run the benchmark in its entirety.
The `envs` folder includes `apptainer` definitions that are used to build the images used by the benchmark.
