#!/bin/bash
#PBS -N aual-ecut
#PBS -q normal
#PBS -l nodes=1:ppn=10

source /app/anaconda3/bin/activate

cd $PBS_O_WORKDIR

mpirun -n 10 gpaw-python scf-ecut.py

