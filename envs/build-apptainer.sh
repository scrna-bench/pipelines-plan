#!/bin/bash

apptainer build r-bioc-320.sif r-bioc-320.def
apptainer build scanpy_full.sif scanpy_full.def
