#!/bin/bash
#PBS -N heptamer-neb
#PBS -q normal
#PBS -l nodes=1:ppn=16

source /app/anaconda3/bin/activate

cd $PBS_O_WORKDIR

mpirun -n 16 gpaw-python neb.py>output

