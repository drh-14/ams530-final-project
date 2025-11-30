#!/bin/bash
#
#SBATCH --job-name=final-project
#SBATCH --ntasks-per-node=36
#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH -p long-40core
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=darren.hamilton@stonybrook.edu

module load openmpi/gcc/64/4.1.2 
mpiexec -n 36 python main.py