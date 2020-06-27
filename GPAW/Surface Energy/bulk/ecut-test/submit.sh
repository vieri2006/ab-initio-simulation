#!/bin/bash
#PBS -N scf-gpaw
#PBS -q normal
#PBS -l nodes=1:ppn=20

source /app/anaconda3/bin/activate

cd $PBS_O_WORKDIR

mpirun -n 20 gpaw-python scf-ecut.py

