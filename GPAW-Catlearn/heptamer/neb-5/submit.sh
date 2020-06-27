#!/bin/bash
#PBS -N heptamer-neb-5
#PBS -q normal
#PBS -l nodes=1:ppn=15

source /app/anaconda3/bin/activate

cd $PBS_O_WORKDIR

mpirun -n 15 gpaw-python neb.py>output

