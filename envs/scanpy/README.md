## Building the Container

```bash
apptainer build scanpy_full.sif scanpy_full.def
```

## Using the Container

```bash
# Run Python script
apptainer exec scanpy_full.sif python script.py

# Interactive Python
apptainer run scanpy_full.sif

# Shell access
apptainer shell scanpy_full.sif
```

---

## Apptainer def file structure info:

### `Bootstrap` and `From`
**What it does:** Specifies the base image for the container.

**here:**
```
Bootstrap: docker
From: python:3.12.9-slim
```
- Uses Docker Hub's official Python 3.12.9 slim image (matches `python=3.12.9` from conda yml)
- `slim` variant provides minimal Debian base

---

### `%labels`
**What it does:** Adds metadata

- Metadata can be viewed with `apptainer inspect scanpy_env.sif`

---

### `%post`
**What it does:** Commands executed during container build.

**here:**

#### System Dependencies
**from Conda:** All the `lib*` packages (libhdf5, libopenblas, etc.)

We install dev libs via `apt-get` that conda bundles:
- Compilers: `gcc`, `g++`, `gfortran`
- Build tools: `cmake`, `make`
- Libraries: `libhdf5-dev`, `libopenblas-dev`, `libigraph-dev`, etc.

**difference from conda:** Conda pins exact library versions (`libhdf5=1.14.3`), but here, use what Debian provides.

#### Python Packages

Use `pip install` with exact version pins for Python packages from conda yml

**Adaptations made:**
- `python-tzdata==2025.1` (conda) → `tzdata` (PyPI) - different package name
- System libraries not installed via pip (handled by apt-get)

---

### `%environment`
**What it does:** Sets environment variables available when container runs.

**here:**
```
%environment
    export LC_ALL=C.UTF-8
    export LANG=C.UTF-8
```
- Ensures UTF-8 encoding for Python

---

### `%runscript`
**What it does:** Default command when running the container with `apptainer run`.

**here:**
```
%runscript
    exec python "$@"
```
- Makes the container executable as a Python interpreter
- Usage: `apptainer run scanpy_env.sif script.py`
