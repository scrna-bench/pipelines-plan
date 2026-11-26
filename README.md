# Benchmarking scRNA pipelines

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18848104.svg)](https://doi.org/10.5281/zenodo.18848104)

A scRNA-seq pipelines benchmark created using [OmniBenchmark](https://omnibenchmark.org).

## Reproducing

OmniBenchmark is required to run this pipeline and can be installed following [this guide](https://docs.omnibenchmark.org/latest/howto/#installation).

The plan uses omnibenchmark api 0.8, pinned in `pixi.toml`. Every module
repository owns its software environments: it locks each `envs/<env>/` (pixi
or rv) and builds it into a `ghcr.io/scrna-bench/<repo>:<env>-<sha>` image.

```{bash}
git clone https://github.com/scrna-bench/pipelines-plan.git
cd pipelines-plan
pixi run validate
# apptainer (default); on a GPU host include the rapids-singlecell modules
pixi run run --cores 8 --with-capability gpu -- --apptainer-args='--nv'
```

### Conda route

The same environments are also exported as pinned conda files (`envs/*.yml`,
synced from the modules with `pixi run sync-envs`). `pixi run run-conda`
generates `benchmark.conda.yaml` (only `software_backend` differs) and runs it
into `out-conda/`. The R envs are solved separately for conda, so some R
package versions differ from the images (e.g. Seurat).

Stages: `DATA` (one module per dataset), `PIPELINE` (one module per
pipeline), `METRIC` (a gather per dataset: metrics and obkit phase timings for
every pipeline run) and `REPORT` (a global gather: `report/metrics.tsv`,
`report/timings.tsv`, `report/plots.html`).

## Citation

If you use this benchmark in your research, please cite it using the information in `CITATION.cff`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
