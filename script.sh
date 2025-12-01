#!/bin/bash
#
#SBATCH --job-name=final-project
#SBATCH --ntasks-per-node=36
#SBATCH --nodes=1
#SBATCH --time=1:00:00
#SBATCH -p short-40core-shared
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=darren.hamilton@stonybrook.edu

python main.py