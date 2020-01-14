#!/bin/bash
#
#SBATCH --job-name=airflow_test
#SBATCH --partition=LM
#SBATCH --ntasks=1
#SBATCH --time=5:00
#SBATCH --mem=100M

srun hostname